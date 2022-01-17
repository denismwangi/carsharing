$(document).ready(function() {
    // <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.4.8/socket.io.min.js"></script>
    // <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
    
    var server='http://127.0.0.1:5000';
	var socket = io.connect(server);

    socket.on('request_car',function(req){
        //Owner gets a notification of another user's interest
        //This function handles these request containing
        // until,duration,pick_up,drop_off data
    });

    socket.on('message',function(msg){
        //An interested user messages the owner of the car
        //This is function that handles receiving of messages
        
    });

    //This function sends a message to a certain user
    //msg ={"userid":userid,"message":text}
    function sendMessage(msg){
        socket.emit('send_message',msg);
    }

});