var canvas = document.getElementById("canvas"),
    ctx = canvas.getContext("2d"),
    width = canvas.width = window.innerWidth,
    height = canvas.height = window.innerHeight;


setup();

draw();

var caneImage;
function setup(){
    caneImage = new Image();
    caneImage.onload = function(){};
    caneImage.src = "http://karlfloersch.appspot.com/static/images/cane1.png";
}


var angle = 180;
var pos = {'x':400,'y':400};
var speed = 1;
var fps = 60;
function draw() {
    setTimeout(function() {
        requestAnimationFrame(draw);
        ctx.clearRect(0,0,width,height);
        moveRect();
        drawBlindMan();
        
    }, 1000 / fps);
}

var counter = 0;
var caneAngle = 0;
function drawBlindMan(){
    ctx.save();

    ctx.translate(pos.x,pos.y); 
    ctx.rotate(angle*Math.PI/180);
    ctx.beginPath();
    ctx.arc(0,0,10,0,2*Math.PI);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(5,2,1,0,2*Math.PI);
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(5,-2,1,0,2*Math.PI);
    ctx.stroke();

    caneAngle = 30*Math.sin(counter);
    ctx.translate(5,-1); 
    ctx.rotate(caneAngle*Math.PI/180);
    ctx.drawImage(caneImage, 5, -1);

    ctx.translate(-pos.x-25,-pos.y-25);

    ctx.restore();

    counter +=.15;
}
var turnSpeed = 1;
function moveRect(){
    pos.x+= speed*Math.cos(angle * Math.PI / 180);
    pos.y+= speed*Math.sin(angle * Math.PI / 180);

    if(pos.x -30 < 0){
        pos.x = 30;
        angle +=turnSpeed;
    }else if(pos.x + 40 > width){
        pos.x = width - 40;
        angle +=turnSpeed;
    }

    if(pos.y - 30< 0){
        pos.y = 30;
        angle +=turnSpeed;
    }else if(pos.y + 30> height){
        pos.y = height-30;
        angle +=turnSpeed;
    }
}
/**
 * Returns a random integer between min and max
 * Using Math.round() will give you a non-uniform distribution!
 */
function getRandomInt (min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function drawCircle(startX, startY, endX, endY) {
    ctx.beginPath();
    ctx.arc(startX,startY,100,0,2*Math.PI);
    ctx.stroke();
}



window.onresize = function () {
    height = canvas.height = document.body.offsetHeight;
    width = canvas.width = document.body.offsetWidth;
};

window.onscroll = function(){
    scrollTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
    console.log("messing");

}


var mousePos = {'x':0, 'y':0};
// ******** UPDATES mousePos WHENEVER MOUSE IS MOVED ******** //
function getMousePos(canvas, evt) 
{
    var rect = canvas.getBoundingClientRect();
    return {
      x: Math.round((evt.clientX-rect.left)/(rect.right-rect.left)*canvas.width),
      y: Math.round((evt.clientY-rect.top)/(rect.bottom-rect.top)*canvas.height)
  };
}

var mp;
canvas.addEventListener('mousemove', function(evt) {
    mp = getMousePos(canvas, evt);
    mousePos.x = mp.x;
    mousePos.y = mp.y;
}, false);
// ******* END UPDATES mousePos WHENEVER MOUSE IS MOVED ******* //

// ^^^^^^^^^^  INPUT INTERPRETATION FUNCTIONS  ^^^^^^^^^^ //




// http://paulirish.com/2011/requestanimationframe-for-smart-animating/
// http://my.opera.com/emoller/blog/2011/12/20/requestanimationframe-for-smart-er-animating
 
// requestAnimationFrame polyfill by Erik Möller
// fixes from Paul Irish and Tino Zijdel
(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame']
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }
 
    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); },
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
 
    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());
