/*
    This file is part of Alpertron Calculators.

    Copyright 2015 Dario Alejandro Alpern

    Alpertron Calculators is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Alpertron Calculators is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Alpertron Calculators.  If not, see <http://www.gnu.org/licenses/>.
*/
/** @define {number} */ var lang = 1;   // Use with Closure compiler.
(function(global)
{   // This method separates the name space from the Google Analytics code.
var points=[0,6, 2,9, 4,0, 5,6, 7,1, 8,0, 13,9, 14,9, 15,7, 16,7, 17,0, 18,13, 20,5, 22,10, 23,12, 24,6, 27,7];
var wizardStep = 0;
var wizardTextInput;
var worker = 0;
var fileContents = null;
var app;
var blob, blobWasm;
var digits;
var config;
var workerParam;
var asmjs = typeof(WebAssembly) === "undefined";
var indexedDBSupport = ('indexedDB' in window);
var db;
function oneexpr()
{
  get("next").value = (lang? "Hecho": "Done");
  get("wzddesc").innerHTML = (lang? "Paso 1 de 1: Expresión a factorizar": "Step 1 of 1: Expression to factor");
  get("wzdexam").innerHTML = "&nbsp;";
  wizardTextInput = "";
  wizardStep = 9;
}

function get(x)
{
  return document.getElementById(x);
}

function setStorage(name, data)
{
  window.localStorage.setItem(name, data);
}

function getStorage(name)
{
  return window.localStorage.getItem(name);
}

function styleButtons(style1, style2)
{
  get("eval").style.display = style1;
  get("factor").style.display = style1;
  get("config").style.display = style1;
  get("openwizard").style.display = style1;
  get("stop").style.display = style2;
  get("more").style.display = style2;
}

function restartFactorization(type)
{
  get("modal-more").style.display = "none";
  if (worker)
  {
    worker.terminate();
  }
  worker = 0;
  dowork(type);
}

function b64decode(str,out)
{
  var ch, idx;
  var idxDest,idxSrc;
  var blocks, left_over;
  var byte0, byte1, byte2, byte3;
  var conv=new Int8Array(128);
  var len=str.length;
  if(str.charAt(len-1)=="=")
  {
    len--;
  }
  if(str.charAt(len-1)=="=")
  {
    len--;
  }
  blocks=len & (-4);
  for (ch = 65; ch <= 90; ch++)   // A - Z
  {
    conv[ch] = ch - 65;
  }
  for (ch = 97; ch <= 122; ch++)  // a - z
  {
    conv[ch] = ch - 71;
  }
  for (ch = 48; ch <= 57; ch++)   // 0 - 9
  {
    conv[ch] = ch + 4;
  }
  conv[43] = 62;                  // +
  conv[33] = 63;                  // !
  for (idxDest=0,idxSrc=0; idxSrc<blocks; idxDest+=3,idxSrc+=4)
  {
    byte0 = conv[str.charCodeAt(idxSrc)];
    byte1 = conv[str.charCodeAt(idxSrc+1)];
    byte2 = conv[str.charCodeAt(idxSrc+2)];
    byte3 = conv[str.charCodeAt(idxSrc+3)];
    
    out[idxDest] = (byte0<<2) + (byte1>>4);
    out[idxDest+1] = (byte1<<4) + (byte2>>2);
    out[idxDest+2] = (byte2<<6) + byte3;
  }
  left_over = len & 3;
  if (left_over == 2)
  {
    byte0 = conv[str.charCodeAt(idxSrc)];
    byte1 = conv[str.charCodeAt(idxSrc+1)];
    
    out[idxDest] = (byte0<<2) + (byte1>>4);
    out[idxDest+1] = byte1<<4;
  }
  else if (left_over == 3)
  {
    byte0 = conv[str.charCodeAt(idxSrc)];
    byte1 = conv[str.charCodeAt(idxSrc+1)];
    byte2 = conv[str.charCodeAt(idxSrc+2)];
    
    out[idxDest] = (byte0<<2) + (byte1>>4);
    out[idxDest+1] = (byte1<<4) + (byte2>>2);
    out[idxDest+2] = byte2<<6;
  }
}

function callWorker(param)
{
  if (!worker)
  {
    if (!blob)
    {
      if (asmjs)
      {    // Asm.js
        blob = new Blob([fileContents]);
      }
      else
      {    // WebAssembly
        blob = new Blob([get("worker").textContent],{type: 'text/javascript'});
      }
    }   
    worker = new Worker(window.URL.createObjectURL(blob));
    worker.onmessage = function(e)
    { // First character of e.data is:
      // "1" for intermediate output
      // "2" for end calculation
      // "4" for sending intermediate data
      // "6" for pausing calculation and showing the Continue button
      // "7" for saving curve number into local storage
      // "8" for saving input expression into local storage
      // "9" for sending data to console.
      var firstChar = e.data.substring(0, 1);
      if (firstChar == "9")
      {
        console.log(e.data.substring(1));
      }
      if (firstChar == "8")
      {
        setStorage("ecmFactors", e.data.substring(1));
        setStorage("ecmCurve", "");
      }
      else if (firstChar == "7")
      {
        setStorage("ecmCurve", e.data.substring(1));
      }
      else if (firstChar == "4")
      {
        get("status").innerHTML = e.data.substring(1);
      }
      else if (firstChar == "5")
      {
        if (e.data.substring(1, 2) == "1")
        {
          get("skip").style.display = "block";
        }
        else
        {
          get("skip").style.display = "none";
        }
      }
      else
      {
        get("result").innerHTML = e.data.substring(1);
        if (firstChar == "2" || firstChar == "6")
        {   // First character passed from web worker is "2".
          get("status").innerHTML = "";
          styleButtons("inline", "none");  // Enable eval and factor
          get("modal-more").style.display = "none";
          if (firstChar == "6")
          {
            get("cont").style.display = "block";
          }
        }
      }
    };
  }
  if (asmjs)
  {      // Asm.js
    worker.postMessage(param);
  }
  else
  {      // WebAssembly.
    worker.postMessage([param, fileContents]);
  }
}

function dowork(n)
{
  var param;
  app = lang + n;
  var res = get("result");
  var valueText = get("value").value.replace(/\u2011/g, "-");
  var charNull = String.fromCharCode(0);
  var helphelp = get("helphelp");
  get("cont").style.display = "none";
  get("help").style.display = "none";
  helphelp.style.display = "block";
  helphelp.innerHTML = (lang ? '<p class="pad">Aprieta el botón <strong>Ayuda</strong> para obtener ayuda para esta aplicación. Apriétalo de nuevo para retornar a la factorización. Los usuarios con teclado pueden presionar CTRL+ENTER para comenzar la factorización. Esta es la versión '+(asmjs? "asm.js": "WebAssembly")+".</p>":
                               '<p class="pad">Press the <strong>Help</strong> button to get help about this application. Press it again to return to the factorization. Keyboard users can press CTRL+ENTER to start factorization. This is the '+(asmjs? "asm.js": "WebAssembly")+" version.</p>");
  res.style.display = "block";
  if (valueText == "")
  {    // Nothing in input box.
    res.innerHTML = (lang ? "<p>Por favor ingrese una expresión.</p>" :
                            "<p>Please type an expression.</p>");
    return;
  }
  if (typeof(Worker) === "undefined")
  {    // Web workers not supported on this browser.
    res.innerHTML = (lang ? "<p>Esta calculadora necesita Web Workers. Por favor use otro navegador Web.</p>" :
                            "<p>This calculator requires Web Workers. Please use another Web browser.</p>");
    return;
  }
  styleButtons("none", "inline");  // Enable "more" and "stop" buttons
  res.innerHTML = (lang ? "<p>Factorizando la expresión...</p>" :
                          "<p>Factoring expression...</p>");
  if (n < -2)
  {
    app += 6;   // Convert to factorization.
  }
  param = digits + "," + app + "," + config.substring(1) + valueText + charNull +
          getStorage("ecmFactors");
  if (n == -1 || n == -2)
  {
    param += "," + get("curve").value;        // Append new curve number typed by user.
  }
  if (n == -3 || n == -4)
  {
    param += ";" + get("curve").value;        // Append new factor typed by user.
  }
  if (!fileContents)
  {
    workerParam = param + charNull;
  }
  else
  {
    callWorker(param + charNull);
  }
}

function selectLoop()
{   
  get("next").value = (lang ? "Siguiente": "Next");
  get("wzddesc").innerHTML = (lang ? "Paso 1 de 5: Valor inicial de x": "Step 1 of 5: Initial value of x");
  get("wzdexam").innerHTML = (lang? "No usar variables <var>x</var> o <var>c</var>. Ejemplo para números de Smith menores que 10000: <code>1</code>": 
                                    "Do not use variables <var>x</var> or <var>c</var>. Example for Smith numbers less than 10000: <code>1</code>");
  wizardStep = 1;
}
  
function wizardNext()
{
  var nextBtn = get("next");
  var wzdDescText = get("wzddesc");
  var wzdExamText = get("wzdexam");
  var wzdInput = get("wzdinput");
  var valueInput = get("value");
  nextBtn.disabled = true;
  switch (++wizardStep)
  {
    case 2:
      wizardTextInput += "x="+wzdInput.value;
      get("mode").style.display = "none";
      wzdDescText.innerHTML = (lang? "Paso 2 de 5: Valor de x para la nueva iteración": "Step 2 of 5: Value of x for new iteration");
      wzdExamText.innerHTML = (lang? "Variables <var>x</var> y/o <var>c</var> requeridas. Ejemplo para números de Smith menores que 10000: <code>x+1</code>":
                                     "Variables <var>x</var> and/or <var>c</var> required. Example for Smith numbers less than 10000: <code>x+1</code>");
      break;
    case 3:
      wizardTextInput += ";x="+wzdInput.value;
      wzdDescText.innerHTML = (lang? "Paso 3 de 5: Condición para finalizar el ciclo": "Step 3 of 5: End loop condition");
      wzdExamText.innerHTML = (lang? "Variables <var>x</var> y/o <var>c</var> requeridas. Ejemplo para números de Smith menores que 10000: <code>x&lt;10000</code>":
                                     "Variables <var>x</var> and/or <var>c</var> required. Example for Smith numbers less than 10000: <code>x&lt;10000</code>");
      break;
    case 4:
      wizardTextInput += ";"+wzdInput.value;
      wzdDescText.innerHTML = (lang? "Paso 4 de 5: Expresión a factorizar": "Step 4 of 5: Expression to factor");
      wzdExamText.innerHTML = (lang? "Variables <var>x</var> y/o <var>c</var> requeridas. Ejemplo para números de Smith menores que 10000: <code>x</code>":
                                     "Variables <var>x</var> and/or <var>c</var> required. Example for Smith numbers less than 10000: <code>x</code>");
      break;
    case 5:
      wizardTextInput += ";"+wzdInput.value;
      nextBtn.value = (lang? "Hecho": "Done");
      nextBtn.disabled = false;
      wzdDescText.innerHTML = (lang? "Paso 5 de 5: Condición para procesar la expresión": "Step 5 of 5: Process expression condition");
      wzdExamText.innerHTML = (lang? "Variables <var>x</var> y/o <var>c</var> requeridas. Ejemplo para números de Smith menores que 10000: <code>sumdigits(x,10) == sumdigits(concatfact(2,x),10) and not isprime(x)</code>":
                                     "Variables <var>x</var> and/or <var>c</var> required. Example for Smith numbers less than 10000: <code>sumdigits(x,10) == sumdigits(concatfact(2,x),10) and not isprime(x)</code>");
      break;
    case 6:
      if (wzdInput.value != "")
      {
        wizardTextInput += ";"+wzdInput.value;
      }
      valueInput.value = wizardTextInput;
      wizardStep = 0;
      get("hex").checked = get("hexW").checked;
      saveConfig();
      get("main").style.display = "block";
      get("wizard").style.display = "none";
      valueInput.focus();
      break;
    default:
      wizardStep = 0;
      valueInput.value = wzdInput.value;
      get("hex").checked = get("hexW").checked;
      saveConfig();
      get("main").style.display = "block";
      get("wizard").style.display = "none";
      valueInput.focus();
      break;
  } 
  if (wizardStep)
  {
    wzdInput.value = "";
    wzdInput.focus();
  }
}

function saveConfig()
{    
  config = "1" +   // Batch mode
           (get("verbose").checked? "1" : "0") +
           (get("pretty").checked? "1" : "0") +
           (get("cunnin").checked? "1" : "0") +
           (get("hex").checked? "1" : "0");
  digits = get("digits").value;
  setStorage("ecmConfig", digits+","+config);
}

function updateVerbose(isVerbose)    
{
  var cssRules = (document.all) ? document.styleSheets[0]['rules']: document.styleSheets[0]['cssRules'];
  var index;
  var len = cssRules.length;
  for (index=0; index<len; index++)
  {
    if (cssRules[index].selectorText === ".verbose")
    {
      cssRules[index].style["display"] = (isVerbose? "inline": "none");
    }
    if (cssRules[index].selectorText === ".terse")
    {
      cssRules[index].style["display"] = (isVerbose? "none": "inline");
    }
  }
}

function endFeedback()
{
  get("main").style.display = "block";
  get("feedback").style.display = "none";
  get("value").focus();   
}

var calcURLs = ["ecmW0000.js",
               "ecm.webmanifest", "ecmc.webmanifest", "ecm-icon-1x.png", "ecm-icon-2x.png", "ecm-icon-4x.png", "ecm-icon-180px.png", "ecm-icon-512px.png", "favicon.ico"];

var url = window.location.pathname;
function fillCache()
{
  // Test whether the HTML is already on the cache.
  caches.open("newCache").then(function(cache)
  {
    cache.match(url).then(function (response)
    {
      if (response === undefined)
      {     // HTML is not in cache.
        UpdateCache(cache);
      }
      else
      {     // Response is the HTML contents.
        var date = response.headers.get('last-modified');
            // Request the HTML from the Web server.
            // Use non-standard header to tell Service Worker not to retrieve HTML from cache.
        fetch(url,{headers:{'If-Modified-Since': date, 'x-calc': '1'}, cache: "no-store"}).then(function(responseHTML)
        {
          if (responseHTML.status != 200)
          {
            return;        // HTML could not be retrieved, so go out.
          }
          if (date == responseHTML.headers.get('last-modified'))
          {
            return;        // HTML has not changed, so other files have not been changed. Go out.
          }
          // Read files to new cache.
          // Use temporary cache so if there is any network error, original cache is not changed.
        
          caches.open("cacheECM").then(function(tempCache)
          {                // Do not fetch HTML because it is already fetched.
            tempCache.addAll(calcURLs).then(function()
            {              // Copy cached resources to main cache and delete this one.
              tempCache.matchAll().then(function(responseArr)
              {            // All responses in array responseArr.
                responseArr.forEach(function(responseTempCache, index, array)
                {
                  var urlTemp = responseTempCache.url;
                  var indexZero = url.indexOf("00");
                  if (indexZero > 0)
                  {        // There is an old version of this resource on cache to be erased.
                    cache.keys().then(function(keys)
                    {
                      keys.forEach(function(requestCache, index, array)
                      {    // Traverse cache.
                        if (requestCache.url.substring(0, indexZero+2) == urlTemp.substring(0, indexZero+2) &&
                            requestCache.url.substring(indexZero+2, indexZero+4) != urlTemp.substring(indexZero+2, indexZero+4) &&
                            requestCache.url.substring(indexZero+4) == urlTemp.substring(indexZero+4))
                        {  // Old version of asset found (different number and same prefix and suffix). Delete it from cache.
                          cache.delete(requestCache);
                        }  
                      });
                      // Put resource into cache after old resource has been erased.
                      cache.put(urlTemp, responseTempCache);
                    });
                  }
                  else
                  {   // Put resource into cache (no old resource into cache). 
                    cache.put(urlTemp, responseTempCache);
                  }
                });
                cache.put(url, responseHTML);
              });
            })
            .finally(function()
            {
              caches.delete("cacheECM");
            });
          })
          .catch (function()     // Cannot fetch HTML.
          {
            UpdateCache(cache);
          });
        })
      }
    });
  });
}

function UpdateCache(cache)
{
  caches.open("cacheECM").then(function(tempCache)
  {
    tempCache.addAll([url].concat(calcURLs)).then(function()
    {     // Copy cached resources to main cache and delete this one.
      tempCache.matchAll().then(function(responseArr)
      {   // All responses in array responseArr.
        responseArr.forEach(function(responseTempCache, index, array)
        {
          cache.put(responseTempCache.url, responseTempCache);
        });
      })
      .finally(function()
      {
        caches.delete("cacheECM");
      });
    });  
  });
}

function startUp()
{
  var param, index, ecmFactor;
  app = lang;
  get("value").wrap="off";
  get("eval").onclick = function ()
  {
    setStorage("ecmFactors","");
    dowork(0);
  };
  get("factor").onclick = function ()
  {
    setStorage("ecmFactors","");
    dowork(2);
  };
  get("more").onclick = function ()
  {
    get("modal-more").style.display = "block";
  };
  get("config").onclick = function ()
  {
    get("digits").value = digits;
    get("verbose").checked = (config.substr(1,1)=="1");
    get("pretty").checked = (config.substr(2,1)=="1");
    get("cunnin").checked = (config.substr(3,1)=="1");  
    get("hex").checked = (config.substr(4,1)=="1");
    get("modal-config").style.display = "block";
  };
  get("openwizard").onclick = function ()
  {
    get("main").style.display = "none";
    get("wizard").style.display = "block";
    get("mode").style.display = "block";
    get("oneexpr").checked = true;
    get("next").disabled = true;
    get("wzdinput").value = "";
    get("wzdinput").focus();
    get("hexW").checked = (config.substr(4,1)=="1");
    get("decW").checked = (config.substr(4,1)!="1");
    oneexpr();
  };
  get("wzdinput").onkeydown = function (event)
  {
    if (event.keyCode == 10 || event.keyCode == 13)
    {
      event.preventDefault();          // Do not propagate Enter key.
      if (get("next").disabled == false)
      {                                // Next button is not disabled.
        wizardNext();                  // Perform same operation as if the user had pressed Next button.
      }
    }
    if (event.altKey)
    {                                  // User pressed ALT key.
      if (event.keyCode == 80)
      {                                // User pressed ALT-P.
        event.preventDefault();        // Do not propagate key.
        if (get("oneexpr").checked)
        {
          get("oneexpr").checked = false;
          get("loop").checked = true;
          selectLoop();
        }
        else
        {
          get("oneexpr").checked = true;
          get("loop").checked = false;
          oneexpr();
        }
      }
      else if (event.keyCode == 68)
      {                                // User pressed ALT-D.
        event.preventDefault();        // Do not propagate key.
        get("decW").checked = true;
        get("hexW").checked = false;
      }
      else if (event.keyCode == 72)
      {                                // User pressed ALT-H.
        event.preventDefault();        // Do not propagate key.
        get("decW").checked = false;
        get("hexW").checked = true;
      }
    }
    return true;
  };
  get("oneexpr").onclick = function ()
  {
    oneexpr();
  };
  get("loop").onclick = function ()
  {
    selectLoop();
  };
  get("next").onclick = function ()
  {
    wizardNext();
  };
  get("wzdinput").oninput = function ()
  {
    var inputValue = get("wzdinput").value;
    var nextBtn = get("next");
    if (inputValue != "")
    {         // User typed something on input box.
      if (wizardStep == 1 || wizardStep == 9 || (inputValue.lastIndexOf("x") >= 0 || inputValue.lastIndexOf("c") >= 0 ||
          inputValue.lastIndexOf("X") >= 0 || inputValue.lastIndexOf("C") >= 0))
      {       // At least one x or c. Indicate valid.
        nextBtn.disabled = false;
      }
      else
      {
        nextBtn.disabled = true;
      }
    }
    else if (wizardStep == 5)
    {         // Last step is optional, so empty input is valid.
      nextBtn.disabled = false;
    }
    else
    {         // For required input, empty input is invalid.
      nextBtn.disabled = true;
    }
  };
  get("cancel").onclick = function ()
  {
    get("main").style.display = "block";
    get("wizard").style.display = "none";
  };
  get("close-config").onclick = function ()
  {
    get("modal-config").style.display = "none";
  };
  get("cancel-config").onclick = function ()
  {
    get("modal-config").style.display = "none";
  };
  get("save-config").onclick = function ()
  {
    saveConfig();
    updateVerbose(get("verbose").checked);
    get("modal-config").style.display = "none";
  };
  get("close-more").onclick = function ()
  {
    get("modal-more").style.display = "none";
  };
  get("ncurve").onclick = function ()
  {
    restartFactorization(-2);
  };
  get("nfactor").onclick = function ()
  {
    restartFactorization(-4);
  };
  get("curve").onkeypress = function(event)
  {
    return (event.charCode == 8 || event.charCode == 0) ? null : event.charCode >= 48 && event.charCode <= 57;
  };
  get("stop").onclick = function ()
  {
    worker.terminate();
    worker = 0;
    styleButtons("inline", "none");  // Enable eval and factor
    get("skip").style.display = "none";  // Hide button if it is present during factorization.
    get("result").innerHTML =
      (lang ? "<p>Cálculo detenido por el usuario.</p>" :
                 "<p>Calculation stopped by user</p>");
    get("status").innerHTML = "";
  };
  get("value").onkeydown = function (event)
  {
    if ((event.keyCode == 10 || event.keyCode == 13) && event.ctrlKey)
    {
      event.preventDefault();          // Do not propagate Enter key.
      setStorage("ecmFactors","");     // Perform factorization.
      dowork(2);
    }
    return true;
  }
  get("helpbtn").onclick = function ()
  {
    var help = get("help");
    var helpStyle = help.style;
    var helphelpStyle = get("helphelp").style;
    var result = get("result");
    var resultStyle = result.style;
    if (helpStyle.display == "block" && result.innerHTML != "")     
    {
      helpStyle.display = "none";
      helphelpStyle.display = resultStyle.display = "block";
    }
    else
    {
      helpStyle.display = "block";
      helphelpStyle.display = resultStyle.display = "none";
    }
  };
  get("skiptest").onclick = function ()
  {
    get("skip").style.display = "none";
    restartFactorization(4);
  }
  get("continue").onclick = function ()
  {
    get("cont").style.display = "none";
    callWorker("C");  // Indicate worker that user pressed Continue button.
  }
  get("formlink").onclick = function ()
  {
    get("main").style.display = "none";
    get("feedback").style.display = "block";
    get("formfeedback").reset();
    get("name").focus();
    return false;   // Do not follow the link.
  }
  get("formcancel").onclick = function ()
  {
    endFeedback();
  }
  get("formsend").onclick = function()
  {
    var userdata = get("userdata");
    if (get("adduserdata").checked)
    {
      userdata.value = "\n" + get("value").value + "\n" + get("result").innerHTML + "\n" + get("status").innerHTML;
    }
    else
    {
      userdata.value = "";      
    }
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function (event)
    {
      if (xhr.readyState == 4) 
      {             // XHR finished.
        if (xhr.status == 200)
        {           // PHP page loaded.
          alert(lang?"Comentarios enviados satisfactoriamente.": "Feedback sent successfully.");
        }
        else
        {           // PHP page not loaded.
          alert(lang?"No se pudieron enviar los comentarios.": "Feedback could not be sent.");
        }
        endFeedback();
      }
    };
    xhr.open("POST", (lang? "/enviomail.php": "/sendmail.php"), true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    var elements = get("formfeedback").elements;
    var contents = "";
    var useAmp = 0;
    for (var i = 0; i < elements.length; i++)
    {
      var element = elements[i];
      if (element.type == "radio" && element.checked == false)
      {
        continue;
      }
      if (element.name)
      {
        if (useAmp)
        {
          contents += '&';
        }
        contents += element.name + "=" + encodeURIComponent(element.value);
        useAmp++;
      }
    }
    xhr.send(contents);
    return false;   // Send form only through JavaScript.
  }
  window.onclick = function(event)
  {
    var modal = get("modal");
    if (event.target == modal)
    {
      modal.style.display = "none";
    }
  };
  // Generate accordion.
  var acc = document.querySelectorAll("h2");
  var idx, x, y;

  for (idx = 0; idx < acc.length; idx++)
  {
    acc[idx].addEventListener("click", function()
    {
    // "active" means that panel is being displayed.
      this.children[0].classList.toggle("active");
      var panel = this.nextElementSibling;
      if (panel.style.display === "block")
      {
        panel.style.display = "none";
      }
      else
      {
        panel.style.display = "block";
      }
    });
  }
  document.getElementById("exprcopy").innerHTML = document.getElementById("exprorig").innerHTML;
  var c = document.getElementById("ellCurve");
  var ctx = c.getContext("2d");
  ctx.fillStyle="#FFFFFF";      // White.
  ctx.fillRect(0,0,313,313);    // Clear canvas.
  ctx.fillStyle="#000000";      // Black.
  ctx.strokeStyle="#808000";
  ctx.fillRect(20,0,290,290);   // Clear canvas.
  for (x=0; x<=290; x+=10)      // Draw grid.
  {
    ctx.moveTo(20+x, 0);
    ctx.lineTo(20+x, 290);
    ctx.stroke();
    ctx.moveTo(20, x);
    ctx.lineTo(310, x);
    ctx.stroke();     
  }
  ctx.fillStyle="#00C000";      // Green.
  var ctr;
  for (ctr=0; ctr<points.length; ctr+=2)
  {
    x = points[ctr];
    y = points[ctr+1];
    ctx.fillRect(20+x*10+1,(28-y)*10+1,9,9);
    if (y != 0)
    {
      ctx.fillRect(20+x*10+1,(y-1)*10+1,9,9); 
    }
  }
  ctx.fillStyle="#000000";      // Black.
  ctx.font = "15px 'Times New Roman'";
  ctx.fillText("0",5,291);
  ctx.fillText("0",20,308);
  ctx.fillText("28",0,11);
  ctx.fillText("28",297,308);
  ctx.font = "italic "+ctx.font;
  ctx.fillText("y",5,150);
  ctx.fillText("x",160,308);  
  digits = getStorage("ecmConfig");
  if (digits == null || digits == "")
  {
    digits = 6;
    config = "00100";
    setStorage("ecmConfig", digits+","+config);
  }
  else
  {
    index = digits.indexOf(",");
    if (index<0)
    {
      digits = 6;
      config = "00100";
      setStorage("ecmConfig", digits+","+config);
    }
    else
    {
      config = digits.substr(index+1);
      while (config.length < 5)
      {  // Convert legacy configuration.
        config += "0";
      }
      digits = digits.substr(0,index);
      updateVerbose(config.substr(1,1) == "1");
    }
  }
  ecmFactor = getStorage("ecmFactors");
  if (ecmFactor)
  {          // Continue factoring.
    get("value").value = ecmFactor.slice(0,ecmFactor.indexOf("="));
    get("curve").value = getStorage("ecmCurve");
    dowork(-2);
    get("curve").value = "";
  }
  
  if ('serviceWorker' in navigator)
  { // Attempt to register service worker.
    // There is no need to do anything on registration success or failure in this JavaScript module.
    navigator["serviceWorker"]["register"]('calcSW.js').then(function() {}, function() {});
    fillCache();
  }
}
if (asmjs)
{
  var req = new XMLHttpRequest();
  req.open('GET', "ecmW0000.js", true);
  req.responseType = "arraybuffer";
  req.onreadystatechange = function (aEvt)
  {
    if (req.readyState == 4 && req.status == 200)
    {
      fileContents = /** @type {ArrayBuffer} */ (req.response);
      if (workerParam)
      {
        callWorker(workerParam);
      }
    }
  };
  req.send(null);
}
else
{
  var wasm = document.getElementById("wasmb64").text;
  while (wasm.charCodeAt(0) < 32)
  {
    wasm = wasm.substring(1);
  }    
  while (wasm.charCodeAt(wasm.length-1) < 32)
  {
    wasm = wasm.substring(0, wasm.length-1);
  }    
  var length = wasm.length*3/4;
  if (wasm.charCodeAt(wasm.length-1)==61)
  {
    length--;
  }
  if (wasm.charCodeAt(wasm.length-2)==61)
  {
    length--;
  }
  fileContents=new Int8Array(length);
  b64decode(wasm, fileContents); 
}
window.addEventListener("load", startUp);
})(this);
