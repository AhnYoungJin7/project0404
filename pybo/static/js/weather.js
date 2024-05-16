function wind_direction(VEC){
    VEC = Number(VEC)
    arr = [
    '북', '북북동', '북동', '동북동' , '동', '동남동', '남동', '남남동', '남', '남남서',
    '남서', '서남서', '서', '서북서', '북서', '북북서', '북'
    ] 
    let convert_vec = Math.floor((22.5*0.5 + VEC) / 22.5)

    return arr[convert_vec]
  }

  function getWeather(){
    let date = new Date();
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    month = month<10? "0"+month:month+""

    let day = date.getDate();
    day = day<10?"0"+day : day+""
    
    s_date = year + ""+month+""+day

    url = "/weather/item/"+s_date+"/서울 강동구 천호제1동";


    $.getJSON(encodeURI(url), function(result){
      console.log(result);
      // 강수형태
      let PTY = result[0]["obsrValue"]
      condition={
          "0":"강수 없음",
          "1":"비",
          "2":"비/눈",
          "3":"눈",
          "5":"빗방울",
          "6":"빗방울눈날림",
          "7":"눈날림"
      }

      $("#PTY").text(condition[PTY]);

      // 기온
      let T1H = result[3]["obsrValue"]
      $("#T1H").text(T1H);

      // 습도
      let REH = result[1]["obsrValue"]
      $("#REH").text(REH);

      // 시간당 강수량
      let RN1 = result[2]["obsrValue"]
      $("#RN1").text(RN1);       
      
      // 풍향
      let VEC = result[5]["obsrValue"]
      VEC = wind_direction(VEC);
      $("#VEC").text(VEC);      
      


      // 풍속
      let WSD = result[7]["obsrValue"]
      $("#WSD").text(WSD);            

    });
  }