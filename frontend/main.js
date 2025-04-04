$(document).ready(function () {
  eel.init()()
  $('.text').textillate({
      loop: true,
      sync: true,
      in: {
          effect: "bounceIn",
      },
      out: {
          effect: "bounceOut",
      },

  });

  //siri
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
    amplitude:"1",
    speed:"0.30",
    autostart: true
  });

  //siri
  $('.siri-message').textillate({
    loop: true,
    sync: true,
    in: {
        effect: "fadeInUp",
        sync: true,
    },
    out: {
        effect: "fadeOutUp",
        sync: true,
    },

});

//mic 

$("#micBtn").click(function () { 
  eel.playAssistantSound()
  $("#Oval").attr("hidden", true);
  $("#SiriWave").attr("hidden", false);
  eel.allCommands()()
});

function doc_keyUp(e) {
  if(e.key==='y' && e.metaKey){
  eel.playAssistantSound()
  $("#Oval").attr("hidden", true);
  $("#SiriWave").attr("hidden", false);
  eel.allCommands()()
  }
}
document.addEventListener('keyup',doc_keyUp,false);

function playAssistantSound(message) {
  if(message!="") {
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    eel.allCommands(message);
    $("#chatbox").val("")
    $("#micBtn").attr('hidden',false);
    $("#sendBtn").attr('hidden',true);
  }
}

function ShowHideButton(message) {
  if(message.length==0) {
    $("#micBtn").attr('hidden',false);
    $("#sendBtn").attr('hidden',true);
  }
  else {
    $("#micBtn").attr('hidden',true);
    $("#sendBtn").attr('hidden',false);
  }
}

$("#chatbox").keyup(function() {
  let message=$("#chatbox").val();
  ShowHideButton(message)
});

$("#sendBtn").click(function() {
  let message=$("#chatbox").val()
  playAssistantSound(message)
});

$("#chatbox").keypress(function (e) {
  key=e.which;
  if(key ==13) {
    let message=$("#chatbox").val()
    playAssistantSound(message)
  }
});

});
