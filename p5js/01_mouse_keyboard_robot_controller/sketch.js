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

let distance_counter = 0.6;
let distance_counter_speed = 0.01;
let distance_min = 0.6;
let distance_max = 0.9;

let rotation_min_rx = -135;
let rotation_max_rx = -45;
let rotation_min_ry = -90;
let rotation_max_ry = 90;
let rotation_min_rz = -45;
let rotation_max_rz = 45;
let rotation_counter_speed = 1;
let rot_rx_counter = -90;
let rot_rx = -90;
let rot_ry_counter = 0;
let rot_ry = 0;
let rot_rz_counter = 0;
let rot_rz = 0;
let smooth_rotation = 0.5;


// osc (see also https://github.com/HybridThingsLab/osc-bridge)
let osc;

// preload
function preload() {
	// load data here
	customFont = loadFont('data/IBM_Plex_Mono/IBMPlexMono-Regular.ttf');
  }

function setup() {

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

	// init custom fonts
	textFont(customFont);

}

function draw() {

	background(0);

	// follow mouse (if pressed)
	if (mouseIsPressed === true) {

		// position

		// check if key pressed
		if (keyIsPressed === true) {

			// DISTANCE

			// 'w'
			if (keyCode === 87) {
				distance_counter += distance_counter_speed;
			// 's
			} else if (keyCode === 83) {
				distance_counter -= distance_counter_speed;
			}
			if(distance_counter >= distance_max){
				distance_counter = distance_max;
			}
			if(distance_counter <= distance_min){
				distance_counter = distance_min;
			}

			// ROTATION
			
			// rot x 
			// key UP and DOWN
			if(keyCode == UP_ARROW){
				rot_rx_counter += rotation_counter_speed;
			}else if(keyCode == DOWN_ARROW){
				rot_rx_counter -= rotation_counter_speed;
			}
			if(rot_rx_counter >= rotation_max_rx){
				rot_rx_counter = rotation_max_rx;
			}
			if(rot_rx_counter <= rotation_min_rx){
				rot_rx_counter= rotation_min_rx;
			}

			// rot y 
			// key 'a' and 'd'
			if (keyCode === 65) {
				rot_ry_counter += rotation_counter_speed;
			}else if(keyCode == 68){
				rot_ry_counter -= rotation_counter_speed;
			}
			if(rot_ry_counter >= rotation_max_ry){
				rot_ry_counter = rotation_max_ry;
			}
			if(rot_ry_counter <= rotation_min_ry){
				rot_ry_counter= rotation_min_ry;
			}

			// rot z
			// key LEFT and RIGHT
			if(keyCode == RIGHT_ARROW){
				rot_rz_counter += rotation_counter_speed;
			}else if(keyCode == LEFT_ARROW){
				rot_rz_counter -= rotation_counter_speed;
			}
			if(rot_rz_counter >= rotation_max_rz){
				rot_rz_counter = rotation_max_rz;
			}
			if(rot_rz_counter <= rotation_min_rz){
				rot_rz_counter= rotation_min_rz;
			}
		}


		// smooth
		pos_x = lerp(pos_x, mouseX, smooth);
		pos_z = lerp(pos_z, mouseY, smooth);
		pos_y = lerp(pos_y, distance_counter, smooth);
		rot_rx = lerp(rot_rx, rot_rx_counter, smooth_rotation);
		rot_ry = lerp(rot_ry, rot_ry_counter, smooth_rotation);
		rot_rz = lerp(rot_rz, rot_rz_counter, smooth_rotation);
		
		// constrain
		pos_x= constrain(pos_x, 0, width);
		pos_z = constrain(pos_z, 0, height);

		// color
		stroke(255, 0, 255);

	}else{

		// color
		stroke(255);
	}

	// viz
	noFill();
	strokeWeight(2);

	push();
	z_position = map(pos_y, distance_min, distance_max, 10, 300);
	translate(pos_x-width/2, pos_z-height/2, z_position);
	rotateX(radians(rot_rx));
	rotateY(radians(rot_ry));
	rotateZ(radians(rot_rz));
	box(50);


	// show x, y, y axis
	let axis_length = 80;
	let axis_width = 3;
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
	let mapped_x = map(pos_x, 0, width, -0.5, 0.5);
	let mapped_z = map(pos_z, 0, height, 1.0, 0.0);

	let message = new OSC.Message("/servopose", mapped_x, pos_y, mapped_z, radians(rot_rx), radians(rot_ry), radians(rot_rz), 1);

	if(mouseIsPressed === true){
		osc.send(message);
	}

	push();
	noStroke();
	fill(255);
	textSize(14);
	text("position: "+mapped_x.toFixed(3)+" "+pos_y.toFixed(3)+" "+mapped_z.toFixed(3),-width/2+40,-height/2+40);
	text("rotation: "+rot_rx.toFixed(3)+"° "+rot_ry.toFixed(3)+"° "+rot_rz.toFixed(3)+"°",-width/2+40,-height/2+60);
	text("press 'w' and 's': pos_y",-width/2+40,-height/2+80);
	text("press ↑ and ↓: rot_x | press → and ←: rot_z | press 'a' and 'd': rot_y",-width/2+40,-height/2+100);
	text("press 's': stop robot",-width/2+40,-height/2+120);
	text("press 't': teach robot (= Freedrive)",-width/2+40,-height/2+140);
	pop();

}

// -------------------------------------------- //

function keyPressed() {

	// console.log(keyCode);

	// 's''
	if (keyCode == 83) {
		let message = new OSC.Message("/stop",0); // send stop
		osc.send(message);
	}

	// 't''
	if (keyCode == 84) {
		let message = new OSC.Message("/teachmode",0); // send teachmode
		osc.send(message);
	}
}
