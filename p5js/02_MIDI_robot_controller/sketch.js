// font
let customFont;

// canvas
var w = 800;
var h = 600;

// position
let pos_x = w/2;
let pos_z = h/2;
let pos_y = 0.0;
let smooth = 0.1;

let pos_x_min = -0.5;
let pos_x_max = 0.5;
let pos_z_min = 0.0;
let pos_z_max = 1.0;
let pos_y_min = 0.6;
let pos_y_max = 0.9;

// rotation
let rot_rx = -90;
let rot_ry = 0;
let rot_rz = 0;

let rot_x_min = -135;
let rot_x_max = -45;
let rot_y_min = -90;
let rot_y_max = 90;
let rot_z_min = -45;
let rot_z_max = 45;
let smooth_rotation = 0.1;

// MIDI
let MIDI_number_sliders = [0,1,2,3,4,5];
let controlValues = [0.5,0.5,0.5,0.5,0.5,0.5];


// osc (see also https://github.com/HybridThingsLab/osc-bridge)
let osc;
let toggle_send = false;

// preload
function preload() {
	// load data here
	customFont = loadFont('data/IBM_Plex_Mono/IBMPlexMono-Regular.ttf');
  }

function setup() {

	// canvas
	canvas = createCanvas(w, h, WEBGL);

	// osc
	osc = new OSC();
    osc.open(); 

	// error & feedback managment from robot
	osc.on('/iknosolution', message => {
        console.log("/iknosolution");
    });   
	osc.on('/posesafetyviolation', message => {
        console.log("/posesafetyviolation");
    });   
	osc.on('/jointsafetyviolation', message => {
        console.log("/jointsafetyviolation");
    });   
	osc.on('/movejointsstart', message => {
        console.log("/movejointsstart");
    });   
	osc.on('/movejointsfinished', message => {
        console.log("/movejointsfinished");
    });  
	osc.on('/stopped', message => {
        console.log("/stopped");
    });  

	// Enable WebMidi.js and trigger the onWebMidiEnabled() function when ready.
	WebMidi.enable()
		.then(onWebMidiEnabled)
		.catch(err => alert(err));
  

	// init custom fonts
	textFont(customFont);

}

function draw() {

	background(0);

	// MIDI to position
	let current_pos_x = controlValues[0];
	let current_pos_y = controlValues[1];
	let current_pos_z = 1.0-controlValues[2];

	// MIDI to rotation
	let current_rot_rx = map(controlValues[3], 0.0, 1.0, rot_x_min, rot_x_max);
	let current_rot_ry = map(controlValues[4], 0.0, 1.0, rot_y_min, rot_y_max);
	let current_rot_rz = map(controlValues[5], 0.0, 1.0, rot_z_min, rot_z_max);

	// smooth
	pos_x = lerp(pos_x, current_pos_x, smooth);
	pos_y = lerp(pos_y, current_pos_y, smooth);
	pos_z = lerp(pos_z, current_pos_z, smooth);
	rot_rx = lerp(rot_rx, current_rot_rx, smooth_rotation);
	rot_ry = lerp(rot_ry, current_rot_ry, smooth_rotation);
	rot_rz = lerp(rot_rz, current_rot_rz, smooth_rotation);

	// visualization
	push();
	translate(pos_x*width-width/2, pos_z*height-height/2, pos_y*500-500);
	rotateX(radians(rot_rx));
	rotateY(radians(rot_ry));
	rotateZ(radians(rot_rz));
	noStroke()
	// show x, y, y axis
	let axis_length = 80;
	let axis_width = 3;
	// end effector
	if(toggle_send){
		stroke(255,0,255);
	}else{
		stroke(255);
	}
	strokeWeight(2);
	noFill();
	box(50);
	noStroke();
	// red
	fill(255, 0, 0);
	translate(-axis_length/2, 0, 0);
	box(axis_length, axis_width, axis_width);
	// green
	fill(0, 255, 0);
	translate(axis_length/2, 0, axis_length/2);
	box(axis_width, axis_width, axis_length);
	// blue
	fill(0, 0, 255);
	translate(0, -axis_length/2, -axis_length/2);
	box(axis_width, axis_length, axis_width);
	pop();

	// osc
	let mapped_x = map(pos_x, 1.0, 0.0, pos_x_min, pos_x_max);
	let mapped_y = map(pos_y, 0.0, 1.0, pos_y_min, pos_y_max);
	let mapped_z = map(pos_z, 1.0, 0.0, pos_z_min, pos_z_max);

	// send osc if active
	if(toggle_send){
		let message = new OSC.Message("/servopose", mapped_x, mapped_y, mapped_z, radians(rot_rx), radians(rot_ry), radians(rot_rz), 1.0);
		//console.log(message);
		osc.send(message);
	}

	// text
	push();
	noStroke();
	fill(255);
	textSize(14);
	text("position: "+mapped_x.toFixed(3)+" "+mapped_y.toFixed(3)+" "+mapped_z.toFixed(3),-width/2+40,-height/2+40);
	text("rotation: "+rot_rx.toFixed(3)+"° "+rot_ry.toFixed(3)+"° "+rot_rz.toFixed(3)+"°",-width/2+40,-height/2+60);
	text("press SPACE to drive robot with servopose: "+toggle_send,-width/2+40,-height/2+80);
	text("press 's': stop robot",-width/2+40,-height/2+100);
	text("press 't': teach robot (= Freedrive)",-width/2+40,-height/2+120);
	pop();

}

// custom functions //
function stop(){
	let message = new OSC.Message("/stop",0); // send stop
	osc.send(message);
	console.log("stop");
}

function teach(){	
	let message = new OSC.Message("/teachmode",0); // send teachmode
	osc.send(message);
	console.log("teach");
}

function toggleSend(){
	if(toggle_send){
		toggle_send = false;
	}else{
		toggle_send = true;	
	}
	console.log("toogle send: "+toggle_send);
}

// keyboard interaction //

function keyPressed() {

	// console.log(keyCode);

	// 's''
	if (keyCode == 83) {
		stop();
	}

	// 't''
	if (keyCode == 84) {
		teach();
	}

	// SPACE
	if (keyCode == 32) {
		toggleSend();
	}
}

// Web MIDI //
function onWebMidiEnabled() {

	// Check if at least one MIDI input is detected. If not, display warning and quit.
	if (WebMidi.inputs.length < 1) {
	  alert("No MIDI inputs detected.");
	  return;
	}
  
	// Add a listener on all the MIDI inputs that are detected
	WebMidi.inputs.forEach(input => {
  
	  input.channels[1].addListener("controlchange", e => { 
		//console.log(`Received 'controlchange' message.`, e.controller.number);
		//console.log(`Received 'controlchange' message.`, e.value);
		for(let i=0; i<MIDI_number_sliders.length; i++){
			if(e.controller.number == MIDI_number_sliders[i]){
				controlValues[i] = e.value;
			}
		}

		// check other control values (stop, teach, toggle send...)

		// stop
		if((e.controller.number == 42) && (e.value == 1)){
			stop();
		}

		// stop
		if((e.controller.number == 45) && (e.value == 1)){
			teach();
		}

		// toggle send
		if((e.controller.number == 41) && (e.value == 1)){
			toggleSend();
		}

	  });


	});
  
  }