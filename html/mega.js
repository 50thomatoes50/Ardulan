var popupdata = [false,0], inputarray=0, pin=0, stats;
$( document ).ready(function() {
  $( "td > div" ).hide();
  $( "div#popup" ).hide();
  $( "td" ).click(function() {
    var pos = $(this).position();
    var pos1 = $(this).parent().position();
    var pos2 = $(this).parent().parent().position();
    var pos3 = $(this).parent().parent().parent().position();
    $( "div#popup" ).show();
    $( "div#popup" ).css("top",(pos1.top+pos2.top+pos3.top)+10);
    console.log("p"+pos.top+" p"+pos1.top+" p"+pos2.top+" p"+pos3.top)
    $( "div#popup" ).css("left",(pos.left+pos1.left+pos2.left+pos3.left));
    $( "div#popup" ).find("p#title").text("Arduino:"+$(this).attr("id"))
    switch ($(this).attr("id")) {
      case "13":
      case "12":
      case "11":
      case "10":
      case "4":
      case "50":
      case "52":
      case "51":
      case "53":
        $( "div#popup" ).find("div#data").text("Broche utilisé par le shield Ethernet");
        $( "div#popup" ).find("footer").text("Modification imposible");
        window['popupdata'] = [false,0]
      break;
      case "0":
      case "1":
      case "14":
      case "15":
      case "16":
      case "17":
      case "18":
      case "19":
      case "20":
      case "21":
        $( "div#popup" ).find("div#data").text("Broche utilisé pour communication");
        $( "div#popup" ).find("footer").text("Modification imposible");
        window['popupdata'] = [false,0]
      break;
    
      default:
        $( "div#popup" ).find("div#data").html("<form id='pinconf' action='' method='post'><input type='hidden' name='ard' value='0'><input type='hidden' name='pin' value='"+$(this).attr("id")+"'>PinMode:  <select id='myselect' name='mode' onchange='pinmode(this.value);'><option value='0'>Output</option><option value='1'>input</option><option value='3'>input vpullup</option><option value='2'>pwm</option>  </select>  <p id='dataform'></p><input type='submit' value='Apply' /></form>")
        $( "div#popup" ).find("footer").text("");
        $( "div#popup" ).find("#myselect").selectedIndex = '1';
        $( "#pinconf" ).submit(function( event ) {
          // If .required's value's length is zero
          event.preventDefault();
          if ( 0 ) {
          } else {
            querry = $.post("/arduino", $("#pinconf").serialize() );
            querry.done(function( html ) {
              $( "div#popup" ).find("div#data").find("p#dataform").html("___");
              pinmode( $("div#popup").find("#myselect").val() , window['popupdata'][1] );
              event.preventDefault();
                     });
            querry.fail(function( jqXHR, textStatus, errorThrown ) {
            $( "div#popup" ).find("div#data").find("p#dataform").text( textStatus+errorThrown );
            event.preventDefault();
            });
          }
      });
        var pin = $(this).attr("id"),arr,stat;
        pin-=2;
        if(pin>18)
          pin-=12;
        arr = parseInt(pin/4);
        while(pin>3)
          pin -=4;
        switch(pin){
          case 0:
            stat=stats[arr];
          break;
          case 1:
            stat=stats[arr]>>2;
          break;
          case 2:
            stat=stats[arr]>>4;
          break;
          case 3:
            stat=stats[arr]>>6;
          break;
        }
        stat = stat & 3
        pinmode( stat , $(this).attr("id"));
        
      break;
    }
    //console.log("posdiv "+(pos.top+pos1.top+pos2.top+pos3.top)+";"+(pos.left+pos1.left+pos2.left+pos3.left))
});
$( "div#popup" ).find('#close').click(function() {
  $( "div#popup" ).hide();
});
actualise();
});


var truc,i=0,j,input,querry;

//var start,get,end;
function inputactu(data,start,stop,divname){
  i=0;
  while(i<=(stop-start))
  {
    j = Math.pow(2, i)
    if(j & data ){
      $(divname).find("#"+String(start+i)).text("1");}
    else{
      $(divname).find("#"+String(start+i)).text("0");}
    i++;
  }
}

function actualise(){
  //start = new Date().getTime();
  querry = $.ajax({
    url: "/arduino?id=0",
  })

  querry.done(function( html ) {
      data = html;
      truc = data.split("|")
    $( "#patate" ).text( html );
    input = truc[0].split(",");
    stats = truc[1].split(",");
    inputactu(parseInt(input[0]),2,7,"#pin0");
    inputactu(parseInt(input[1]),8,9,"#pin1");
    inputactu(parseInt(input[2]),22,29,"#pin3");
    inputactu(parseInt(input[3]),30,37,"#pin3");
    inputactu(parseInt(input[4]),38,45,"#pin3");
    inputactu(parseInt(input[5]),46,49,"#pin3");
    if (window['popupdata'][0]===true) {
          var i = window['popupdata'][1];
          if (i>10) {
            i-=6;
          }
          inputarray=0;
          while(i>=8)
          {
            i -= 8;
            inputarray += 1;
          }
          //$( "div#popup" ).find("div#data").find("p#dataform").html(inputarray+" "+i);
          //$( "div#popup" ).find("div#data").find("p#dataform").html(inputarray+" "+i);
          if (window['popupdata'][1] <8) {
            i-=2;
          }
          if (input[inputarray] & Math.pow(2,i)) {
            $( "div#popup" ).find("div#data").find("p#dataform").text("5V (>IOREF)");
          }
          else
            $( "div#popup" ).find("div#data").find("p#dataform").text("GND (<IOREF)");
          
        }
    setTimeout(actualise, 1000);
  });
  querry.fail(function( jqXHR, textStatus, errorThrown ) {
    $( "#patate" ).text( textStatus+errorThrown );
    setTimeout(actualise, 1000);
  });
  //get = new Date().getTime()

  /*end = new Date().getTime();
  console.log("total time = "+(end-start)+" Get="+(get-start)+" DOM="+(end-get))*/
}
function pinmode( value, pin){
  $( "div#popup" ).find("div#data").find("option[value='"+value+"']").attr("selected","selected");
  switch(value){
    case 1:
    case 3:
    case '1':
    case '3':
      window['popupdata'] = [true,pin];
      $( "div#popup" ).find("div#data").find("p#dataform").html("....");
    break;
    
    case 0:
    case '0':
      window['popupdata'] = [false,pin];
      $( "div#popup" ).find("div#data").find("p#dataform").html('<input type="radio" name="data" value="1">5V<br><input type="radio" name="data" value="0">GND');
    break;
  
    case 2:
    case '2':
      window['popupdata'] = [false,pin];
      $( "div#popup" ).find("div#data").find("p#dataform").html("<i>PWM not available in this version</i>");
    break;
    default:
      alert("Value = "+value+" "+typeof value)
  }
}