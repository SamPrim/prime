$(function() {

   /* $(document).delegate(".chat-btn", "click", function() {
      var value = $(this).attr("chat-value");
      var name = $(this).html();
      $("#chat-input").attr("disabled", false);
      generate_message(name, 'self');
    })*/
    var id= $('#pk').attr('pk')//document.getElementById('pk').getAttribute('pk')
    console.log(id)
      $("#chat-circle").click(function() {    
        $("#chat-circle").toggle('scale');
        $(".chat-box").toggle('scale');
    })
          
    $(".chat-box-toggle").click(function() {
      $("#chat-circle").toggle('scale');
      $(".chat-box").toggle('scale');
    })
    setTimeout(function() {      
      generate_message("Bonjour, Je suis Leo\n que puis je faire pour vous?", 'user','/static\/img\/leo.png');
    }, 1000)
      var chatSocket = new ReconnectingWebSocket(
        'ws://localhost:8000/ws/anime/' + id);
      console.log("bienvenu")

    chatSocket.onmessage = function(e) {
      var data = JSON.parse(e.data);
      var response = data['response'];
      console.log("Bien recu: "+response)
      setTimeout(function() {      
        generate_message(response, 'user','/static\/img\/leo.png');
      }, 1000)

      //document.querySelector('#bot-msg').innerText += (response+'\n');
    };

    chatSocket.onclose = function(e) {
        document.querySelector('#bot-msg').innerText += "J'ai pas bien compris"
        console.error('Chat socket closed unexpectedly\n');
    };

    document.querySelector('#chat-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#chat-input');
        var message = messageInputDom.value;
        console.log("bien envoyé: "+message)
        var message = $("#chat-input").val(); 
        if(message.trim() == ''){
          return false;
        }
        generate_message(message, 'self','/static\/img\/leo-sm.png');
        //document.getElementById('user-msg').innerText += (message+'\n');
        chatSocket.send(JSON.stringify({
            'message': message
    }));
    messageInputDom.value =""
  }


  var INDEX = 0; 
 /* $("#chat-submit").click(function(e) {
    e.preventDefault();
    var msg = $("#chat-input").val(); 
    if(msg.trim() == ''){
      return false;
    }
    generate_message(msg, 'self','/static\/img\/leo.png');
    // variable inutile
    /*var buttons = [
        {
          name: 'Existing User',
          value: 'existing'
        },
        {
          name: 'New User',
          value: 'new'
        }
      ];*/ // fin
  /*  setTimeout(function() {      
      generate_message(msg, 'user','/static\/img\/leo-sm.png');  
    }, 5000)
    
  })*/
  
  function generate_message(msg, type, photo) {
    INDEX++;
    var str="";
    str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
    str += "          <span class=\"msg-avatar\">";
    str += "            <img src="+photo+">";
    str += "          <\/span>";
    str += "          <div class=\"cm-msg-text\">";
    str += msg;
    str += "          <\/div>";
    str += "        <\/div>";
    $(".chat-logs").append(str);
    $("#cm-msg-"+INDEX).hide().fadeIn(300);
    if(type == 'self'){
     $("#chat-input").val(''); 
    }    
    $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);    
  } 
  })