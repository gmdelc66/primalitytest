/*
    ULAM SPIRAL
    Copyright(C) 2018 Dario Alejandro Alpern

    This program is free software: you can redistribute it and/or modify
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

// In order to reduce the number of files to read from Web server, this 
// Javascript file includes both the Javascript in the main thread and the 
// Javascript that drives WebAssembly on its own Web Worker.
(function(global)
{   // This method separates the name space from the Google Analytics code.
var buffer, globals, env, asm;
var zoom, zoomDone, imgData;
var canvas, zoomin, zoomout, center, start;
var isMouseDown;
var currentX, currentY, pixels;
var HEAP8, HEAPU8;
var asmjs = typeof(WebAssembly) === "undefined";
var ShowInformation;
var prevX1stTouch, prevY1stTouch;
var prevX2ndTouch, prevY2ndTouch;
// Webassembly module encoded in Base64.
var wasm="AGFzbQEAAAABMQlgAn9/AGAAAGABfwBgA39/fwBgAX8Bf2ACf38Bf2AEf39/fwBgAAF/YAR/f39/AX8CEQEDZW52CV9zaG93SW5mbwAAAxkYAQIDAwMDAwEEAwUDAwAGBQQHBQUDAAAIBAQBcAAABQQBAJACB18GBm1lbW9yeQIAFl9kcmF3UGFydGlhbFVsYW1TcGlyYWwADwpfZ2V0UGl4ZWxzABIQX1Nob3dJbmZvcm1hdGlvbgAWC19tb3ZlU3BpcmFsABcLX25ickNoYW5nZWQAGAqLPhhtAQN/QQAhAQJAA0AgAUEZRg0BIAFBgIWACGosAAAiAEECbUEBaiECAkADQCACQQBIDQEgAUGEA2wgAiACbCAAb0ECdGpBoIWACGpBATYCACACQX9qIQIMAAsLIAFBAWohAQwACwtBAEEBOgAYC6kDBQF/AXwDfwF8An9BACEHIAAoAgi3RAAAAAAAAOBBoiAAKAIEt6AgACgCALdEAAAAAAAAAD6ioEEAKAIct0QAAAAAAAAAPqJBACgCILego0QAAAAAAADgP6CcqyIIQf////8HIAhB/////wdJGyIBtyECRAAAAAAAAAAAIQZBACEIAkADQCAHQQhGDQEgACAHaiIEIAQoAgAiBCAIaiAHQRxqKAIAIgMgAWxrQf////8HcSIFNgIARAAAAAAAAMBBRAAAAAAAAMDBIAVBgICAgARJGyAGIAS3IAIgA7eioSAIt6CgIgZEAAAAAAAA0EOgIAYgBkQAAAAAAAAAAGMiBBugRAAAAAAAAAA+opyqIQhEAAAAAAAA4MFEAAAAAAAAAAAgBBshBiAHQQRqIQcMAAsLIABBCGoiByAHKAIAIAhqQf////8HcSIHNgIAAkAgB0UNAEEAIQdBACEIAkADQCAHQQhGDQEgACAHaiIEIAQoAgAgCGogB0EcaigCAGoiCEH/////B3E2AgAgCEEfdiEIIAdBBGohBwwACwsgAEEIakEANgIACwu1AgMGfwF8BH9BAEEAKAIEQRBrIg02AgQgDUIANwMIIA1CADcDACANQQRyIQNBACEKQQAhC0EAIQwCQANAIApBCEYNASANIApqIgcgASgCACIFIAAgCmooAgAiBGwgDGpB/////wdxIgY2AgAgB0EEaiAEIAFBBGooAgAiCGwgC2ogBLciCSAFt6IgDLegRAAAAAAAAMBBRAAAAAAAAMDBIAZBgICAgARJG6BEAAAAAAAAAD6iqyIEakH/////B3EiDDYCACAHQQhqRAAAAAAAAMBBRAAAAAAAAMDBIAxBgICAgARJGyAJIAi3oiAMt6AgBLigoEQAAAAAAAAAPqKrIgs2AgAgCkEEaiEKDAALCyADEAIgDRACIAIgDSkDADcCACACIA0oAgg2AghBACANQRBqNgIEC9ACBAJ/A34BfwN+AkACQEEAKAIgIgNFDQBBACgCJCIIIAA1AgAiCyABNAIAIgZ+IgenbEH/////B3GtIgkgA6wiCn4gCyABNAIEIgV+fCAJQQAoAhwiBKwiC34gB3xCH4h8IgdCH4hC/////w+DIAA1AgQiCSAFfnwgCCAHQv////8HgyAJIAZ+fCIGp2xB/////wdxrSIHIAp+fCAHIAt+IAZ8Qh+IfCILp0H/////B3EhASALQh+IpyEAAkAgCyADQQFqrEIfhloNACADIABHDQIgASAESQ0CCyAAIANrIAEgBGsiAUEfdWpB/////wdxIQAgAUH/////B3EhAQwBCyABKAIAIQEgACgCACEAAkACQEEAKAIcIgNB//8BSg0AIAEgAGwgA28hAQwBCyABrCAArH4gA6yBpyEBC0EAIQALIAIgADYCBCACIAE2AgALOgEBfyACIAEoAgAgACgCAGoiA0H/////B3E2AgAgAiADQR92IAAoAgRqIAEoAgRqQf////8HcTYCBAs6AQF/IAIgACgCACABKAIAayIDQf////8HcTYCACACIANBH3UgACgCBGogASgCBGtB/////wdxNgIEC4QBAQN/IAEoAgAgACgCAGoiBEH/////B3EhBUEAKAIcIQMCQAJAIARBH3YgACgCBGogASgCBGoiAUEAKAIgIgBLDQAgBSADSA0BIAEgAEcNAQsgASAAayAFIANrIgVBH3VqIQEgBUH/////B3EhBQsgAiAFNgIAIAIgAUH/////B3E2AgQLcAECf0EAQQA2AiwCQEEAKAIgRQ0AQQBBATYCMEEAQQJBAkECQQJBACgCHCIAIABsayAAbCIBIABsayABbCIBIABsayABbCIBIABsa0EAIAFrbEH/////B3E2AiRBAEEANgIoQSgQAg8LQQBBATYCKAuOBwEMf0EAQQAoAgRBIGsiDDYCBEEAIQtBACAAKAIAIgE2AhxBACAAKAIEIgI2AiACQAJAAkACQCACDQAgAUEBRg0DIAFBAkYNAQsgAUEBcUUNAkEBIQcCQANAIAdBGEsNASAHQYCFgAhqLAAAIQACQAJAIAJFDQBBgICAgHggAHAgAiAAcGwgASAAcGogAHANAQwGCyABIABGDQMgASAAcEUNBQsgB0EBaiEHDAALCxAIIAxBACkCKDcCGCABQf7///8HcSIAIAIgABsiByAHQRB2IAdB//8DcSIJGyIHIAdBCHYgB0H/AXEiCxsiByAHQQR2IAdBD3EiAxsiByAHQQJ2IAdBA3EiBxtBf3NBAXFBAEEfIAAbIgAgAEEQaiAJGyIAIABBCGogCxsiACAAQQRqIAMbIgAgAEECaiAHG2ohA0EBIAIgASACGyIAQRB2IAAgAEH//wNLIgcbIgBBCHYgACAAQYD+A3EiCRsiAEEEdiAAIABB8AFxIgsbIgBBAnYgACAAQQxxIggbQQF2QQFxQR9BACACGyIAQRBqIAAgBxsiAEEIaiAAIAkbIgBBBGogACALGyIAQQJqIAAgCBtqIgVBH290IQYgAkEARyEEQQAhCEEBIQlBACEKDAELQQEhCwwBCwNAAkAgCEECdCIHQQRyQZDRgAhqKAIAIgAgAkgNAEEBIQsgACACRw0CIAdBkNGACGooAgAgAU4NAgsgCkHg0YAIaiwAACEAA0AgDEEYakEoIAxBGGoQByAJQQFqIgkgAEkNAAsgDCAMKQIYNwIQIAUhACAEIQsgBiEHAkADQCAAIANMDQEgAEF/aiEAIAxBEGogDEEQaiAMQRBqEAQgCyAHQQF2IgdFayILQQJ0QRxqKAIAIAdBgICAgAQgBxsiB3FFDQAgDEEQaiAMQRhqIAxBEGoQBAwACwsCQAJAIAwoAhBBACgCKEcNACAMQRBqQQRqKAIAQQAoAixGDQELIAxBEGpBKCAMQQhqEAcgDCgCCCAMQQhqQQRqIgcoAgByRQ0AA0BBACELIABBf2oiAEEASA0DIAxBEGogDEEQaiAMQRBqEAQCQCAMKAIQQQAoAihHDQBBACELIAxBEGpBBGooAgBBACgCLEYNBAsgDEEQakEoIAxBCGoQByAMKAIIIAcoAgByDQALCyAIQQJqIQggCkEBaiEKDAALC0EAIAxBIGo2AgQgCwsiACACIAEgAGxB/////wdxNgIAIAIgAawgAKx+Qh+IPgIEC+wCAwJ/AnwDfyABKAIEIgIhBiABKAIAIgEhBwJAIAJBgICAgARxIgNFDQBBACABayIGQf////8HcSEHIAZBH3UgAmtB/////wdxIQYLQQAhCAJAAkAgBrdEAADA////30GiIAe3oCIERAAAAAAAADBAoiAERAAAAAAAADDAoiADGyAAIABst6AiBEQAAAAAAAAAAGMNAEEAIQhBACAAa7ciBSAEn0QAAAAAAADgP6CqtyIEoUQAAAAAAADQP6KqIQYgAkEBdCIDIAUgBKBEAAAAAAAA0D+iqiICQQF0IABqIgesIAKsfkIfiKdqIAcgAmxB/////wdxIAFqIgJBH3ZqIAJB/////wdxIAFqIgJBH3ZqIAJyQf////8HcUUNAQsgCA8LIAMgBkEBdCAAaiIArCAGrH5CH4inaiAAIAZsQf////8HcSABaiIAQR92aiAAQf////8HcSABaiIAQR92aiAAckH/////B3FFC58CAQZ/QQBBACgCBEEQayIINgIEAkACQEEAIAFrIgMgAEoNACAAQQBIDQAgACABSA0AIABBAnRBA3IiBiAAbCEFIAAhByABIQAMAQsCQCABQQBIDQAgACABTg0AQQAgAGsiBCABTg0AIAFBAnRBfWoiBiABbCEFIAEhByAEIQAMAQsCQCADIABIDQAgAEEASg0AIAAgAUoNACAAQQJ0QQFyIgYgAGwhBSAAIQcgAyEADAELIAFBAnRBf2oiBiABbCEFIAEhBwsgAiAFQf////8HcTYCACACIAesIAasfkIfiD4CBCAIIABB/////wdxNgIIIAggAEEfdUH/////B3E2AgwgAiAIQQhqIAIQBSACQRAgAhAFQQAgCEEQajYCBAtaAQF/QQBBACgCBEEQayIDNgIEIANBADYCDAJAAkAgAUEASA0AIAMgATYCCCAAIANBCGogAhAFDAELIANBACABazYCCCAAIANBCGogAhAGC0EAIANBEGo2AgQLtAcDBn8Bfgh/QQBBACgCBEEgayIQNgIEIAAgASAQQRhqEAxBgIB8QYCAgHhBACgCNBshBUEAKAJEQQJtIAFBACgCSGtBACgCDCINdGtBACgCTGohDCAAQQAoAjxrIA10QQAoAjhBAm1qQQAoAkBrIQICQAJAAkAgECgCHCILQQBHIBAoAhgiDUECR3JBAUcNACANQQFxRQ0BC0GAgIN4IQogEEEYahAJDQFBACABayEKAkACQCAAIAFMDQAgACEPIAogAEgNAQsCQCAAIAFODQAgCiAATA0AQQAgAGshDwwBCyABIAogAUEAShshDwsgECANIA9BAXQiCiAKbGsiDUH/////B3EiBzYCACAQIA1BH3UgC2ogCqwiCCAIfkIfiKdrQf////8HcSINNgIEAkACQAJAAkAgASAAakEASA0AIAAgAU4NASAQIA9BAnQgEEEQahANIBAgCiAQQQhqEA1BfiELQXwhDSAQQRBqIQoMAwsgECANNgIUIBAgBzYCECAAIAFODQEgECAKIBBBCGoQDUF+IQtBACENIBBBEGohCgwCC0ECIQsgEEEAIA9BAnRrIBBBEGoQDSAQQQAgCmsgEEEIahANQQQhDSAQQRBqIQoMAQtBACENIBBBACAKayAQQQhqEA1BAiELIBBBEGohCgsgDSAKEAsNACAFQYCAgHggCyAQQQhqEAsbIQoMAQsgBSEKC0EAKAJEIg1BAUEAKAIMIgN0IgUgDGoiBiAGIA1KIgkbIQdBACgCOCIEIAUgAmoiDSANIARKGyEFIAJBACACQQBKGyEPIAxBACAMQQBKGyIOIQsCQANAIAsgB04NASALQQt0IA9qQQJ0QdAAaiENIA8hDAJAA0AgDCAFTg0BIA0gCjYCACAMQQFqIQwgDUEEaiENDAALCyALQQFqIQsMAAsLAkAgA0ECSA0AAkACQCAAIABBH3UiDGogDHMiDSABIAFBH3UiDGogDHMiCk4NACABQQBKIAFBf2ogAEZxDQIgBkEBSA0CDAELAkAgAUF/SkEAIAFrIABHckEBRw0AIAJBAEgNACACIARODQAgDkELdCACakECdEHQAGohDANAIA4gB04NASAMQcCBg342AgAgDkEBaiEOIAxBgMAAaiEMDAALCyABQQBKDQEgDSAKRw0BIAZBAUgNAQsgCQ0AIA8gBkELdGpBAnRB0EBqIQwDQCAPIAVODQEgDEHAgYN+NgIAIA9BAWohDyAMQQRqIQwMAAsLQQAgEEEgajYCBAuWAQEDfwJAQQAtABgNABABC0EAKAJAIgUgAWpBACgCDCIBdUEAKAI8IgZqIQQgBSAAaiABdSAGaiEAQQAoAkgiBUEAQQAoAkxrIgYgA2sgAXVrIQMgBSAGIAJrIAF1ayECAkADQCAAIARKDQEgAiEBAkADQCABIANKDQEgACABEA4gAUEBaiEBDAALCyAAQQFqIQAMAAsLCzsBA39BACEEAkADQCAAIARqIQIgASAEai0AACIDRQ0BIAIgAzoAACAEQQFqIQQMAAsLIAJBADoAACAACx8BAX8gAEF/aiEBA0AgAUEBaiIBLQAADQALIAEgAGsLBQBB0AALiQEBA38CQCABQX9KDQAgAEEtOgAAIABBAWohAEEAIAFrIQELQQAhBEGAlOvcAyEDA0ACQCABIANtIgIgBHJFDQAgACACQTBqOgAAQQEhBCAAQQFqIQAgASACIANsayEBCyADQRNKIQIgA0EKbSEDIAINAAsgAEEAOgABIAAgAUEwajoAACAAQQFqC+IBAwF/AXwCfyABKAIEIQUgASgCACEEQRIhAQJAA0AgAUF/Rg0BIAAgAWogBSAFQQptIgJBCmxrt0QAAAAAAADgQaIgBLegIgMgA0QAAAAAAAAkQKOqIgS3RAAAAAAAACRAoqGqQTBqOgAAIAFBf2ohASACIQUMAAsLQQAhBQJAA0AgBUERSw0BIAAgBWotAABBMEcNASAFQQFqIQUMAAsLIAAgBWohBEEAIQECQANAIAUgAWpBEksNASAAIAFqIAQgAWotAAA6AAAgAUEBaiEBDAALCyAAIAFqIgFBADoAACABC88NBQF/AXwBfwJ8BX9BAEEAKAIEQRBrIgw2AgRBz4CACCEKA0AgCkEBaiIKLQAADQALIAohCwJAA0AgAC0AACIDRQ0BIAsgAzoAACALQQFqIQsgAEEBaiEADAALCyALQQA6AAAgCkECaiEAA0AgAEF+aiELIABBAWoiCiEAIAstAAANAAsgDCACKAIAIgM2AgggDCACKAIEIgs2AgwgCkF9aiEAAkAgCyADckUNACAKQX5qIQkgAEEgOgAAIApBf2ohAAJAAkAgC0GAgICABHENACAAQSA6AAAgCUErOgAAIAxBDGooAgAhCyAMKAIIIQMMAQsgAEEgOgAAIAlBLToAACAMQQxqQQAgA2siAEEfdSALa0H/////B3EiCzYCACAMIABB/////wdxIgM2AggLIAogDEEIahAUIQALAkAgAyABciALckUNAAJAAkACQAJAAkACQAJAAkAgASACEAtFDQBBACABa7ciByALt0QAAMD////fQaIgA7egIgZEAAAAAAAAMECiIAZEAAAAAAAAMMCiIAJBB2otAABBwABxGyABIAFst6CfRAAAAAAAAOA/oKq3IgahRAAAAAAAANA/oiEEIAcgBqBEAAAAAAAA0D+iIQcgAEF/aiEAA0AgAEEBaiIALQAADQALIASqIQogB6oiA0EBSA0BIABBCGpBAC8A+NGACDsAACAAQQApAPDRgAg3AABBICELAkADQCALQf8BcUUNASAAQQFqLQAAIQsgAEEBaiEADAALCyAAIAMQEyEADAYLIAxBCGpBBGogAkEEaiIIKAIAIgo2AgAgDCACKAIAIgs2AgggC0EBcQ0BQQMhAyALIAFyQQNxRQ0DIABBDWpBACkAzdKACDcAACAAQQhqQQApAMjSgAg3AAAgAEEAKQDA0oAINwAAQR4hAkEBIQlBAiEFQQIhAwwECyADQX9MDQEgAEEEakEALwCU0oAIOwAAIABBACgAkNKACDYAAEEgIQsDQCALQf8BcUUNBiAAQQFqLQAAIQsgAEEBaiEADAALC0FnIQpBoIWACCEDQQEhBQJAA0AgCkUNAQJAIAMgASAKQZmFgAhqLAAAIgtvIgkgCWwgAigCACALb0GAgICAeCALcCAIKAIAIAtvbGogC3BBBHRrIAtvIAtqIAtvQQJ0aigCAA0AIABBKEEgIAUbOgABIABBIEEsIAUbOgAAIABBAmogCxATIQBBACEFCyADQYQDaiEDIApBAWohCgwACwsgBQ0FIABBKTsAACAAQQFqIQAMBQsgAEEIakEALwCI0oAIOwAAIABBACkAgNKACDcAAEEgIQsCQANAIAtB/wFxRQ0BIABBAWotAAAhCyAAQQFqIQAMAAsLIABBACADaxATIQAMAgsgAEEQakEAKACw0oAINgAAIABBCGpBACkAqNKACDcAACAAQQApAKDSgAg3AABBHSECQQIhCUEEIQULIAxBDGogCkEBdCADdSIDNgIAIAwgCiACdCALIAl1ckH/////B3E2AgggAEF/aiEAA0AgAEEBaiIALQAADQALIABBAWohCwJAAkACQAJAIAEgBW0iCkUNACAKQX9MDQEgAEGg1oABNgAADAILIAshCiAAIQsMAgsgAEGg2oABNgAAQQAgCmshCgtBICEAAkADQCAAQf8BcUUNASALLQAAIQAgC0EBaiELDAALCyALQX9qIQACQCAKQQFGDQAgACAKEBMiAEEBaiELCyAAQfQAOwAAIAtBAWohCgsgC0EgOgAAAkACQCADQYCAgIAEcQ0AIApBKzoAACALQQJqQSA6AAAMAQsgCkEtOgAAIAtBAmpBIDoAACAMQQxqIgBBACAMKAIIayIKQR91IAAoAgBrQf////8HcTYCACAMIApB/////wdxNgIICyALQQNqIAxBCGoQFCELA0AgCy0AACEKIAtBAWoiACELIAoNAAsgAEF/akEpOwAADAILIABBKToAACAAQQFqIQALAkAgCkEBSA0AIABCoNDIoYfkihA3AABBICELAkADQCALQf8BcUUNASAAQQFqLQAAIQsgAEEBaiEADAALCyAAIAoQEyIAQSk6AAAgAEEBaiEADAELAkAgCkF/TA0AIABBoOTQAzYAAEEgIQsDQCALQf8BcUUNAiAAQQFqLQAAIQsgAEEBaiEADAALCyAAQqDQyKGHpIsQNwAAQSAhCwJAA0AgC0H/AXFFDQEgAEEBai0AACELIABBAWohAAwACwsgAEEAIAprEBMiAEEpOgAAIABBAWohAAsgAEEEakEALQDk0oAIOgAAIABBACgA4NKACDYAAEEAIAxBEGo2AgQLsAUDAn8BfgJ/QQBBACgCBEEgayIGNgIEQQBBADoA0ICACAJAAkACQAJAIABBf0wNAEEAKAJAIABqQQAoAjhBfm1qQQAoAgwiAHVBACgCPGoiAkEAKAJIQQAoAkwgAWtBACgCREECbWogAHVqIgBBAWoiASAGQRhqEAwgAEF/cyEAAkAgAiABTA0AIAIhBSACIABKDQMLIAIgAU4NASACIABODQFBACACayEFDAILIAZBGGohAAwCCyABIAAgAUEAShshBQsgBiAGKAIYIAVBAXQiACAAbGsiA0H/////B3E2AhAgBiADQR91IAYoAhxqIACsIgQgBH5CH4ina0H/////B3E2AhQCQAJAAkACQCABIAJqQQBIDQAgAiABSA0BIAZBEGpBACAFQQJ0ayAGQQhqEA1B8NKACEEEIAZBCGoQFSAGQRBqQQAgAGsgBkEIahANQZDTgAhBAiAGQQhqEBUMAwtB8NOACEEAIAZBEGoQFSACIAFIDQEgBkEQakEAIABrIAZBCGoQDUGQ1IAIQQIgBkEIahAVDAILIAZBEGogBUECdCAGQQhqEA1BsNOACEF8IAZBCGoQFSAGQRBqIAAgBkEIahANQdDTgAhBfiAGQQhqEBUMAQsgBkEQaiAAIAZBCGoQDUHQ04AIQX4gBkEIahAVC0HPgIAIIQADQCAAQQFqIgAtAAANAAsgAEH4+gA7AAAgAEHQgIAIa0HSgIAIaiACEBMiAEGswOTrAzYAACAAQQRqIAEQEyIAQazAuOsDNgAAIABBvMQBOwAEIABBPjoABiAAQQdqIAZBGGoQFCIAQrzeiPPDhYi6PTcAACAAQQhqIAUQExogBkEYaiEAC0EAKAI8QQAoAkggABAMQdCEgAggABAUGkHQgIAIQdCEgAgQAEEAIAZBIGo2AgQLVQECf0EAQQAoAjxBACgCQCAAayICQQAoAgwiAHVqNgI8QQBBASAAdEF/aiIDIAJxNgJAQQBBACgCTCABaiIBIANxNgJMQQBBACgCSCABIAB1ajYCSAvkBAEDf0EAQQAoAgRBEGsiBjYCBEEAIQVBACADNgJEQQAgAjYCOEEAIQNBACECAkADQCAFQRJLDQEgACAFaiwAACIERQ0BIANBCmwgArdEAAAAAAAAJECiIARBUGoiBLegRAAAAAAAAAA+oqpqIQMgBUEBaiEFIAQgAkEKbGpB/////wdxIQIMAAsLAkACQAJAAkACQAJAAkAgAUECRg0AIAFBAUcNASADQQAoAhRrIAJBACgCEGsiBUEfdWoiAyAFQQFqIgJyQf////8HcUUNBCACIANB/////wdxt0QAAAAAAADgQaIgAkH/////B3G3oEQAAAAAAADwv6CfqkEBakECbSIFIAVsQQJ0ayICQf////8HcSIDQYGAgIB4aiADIAJBgICAgARxGyICQQIgBUEBdGtODQJBACAFQX1sQQFqIAJrNgI8DAMLQQAgAzYCFEEAIAI2AhAMBAtBACgCDCEFAkACQCABQQNHDQAgBUEFRg0GQQAgBUEBajYCDEEAQQAoAkBBAXQ2AkBBACgCTEEBdCEFDAELIAVFDQVBACAFQX9qNgIMQQBBACgCQEEBdTYCQEEAKAJMQQF1IQULQQAgBTYCTAwDC0EAIAVrIQMCQAJAIAJBAEwNACACIAVBAXRMDQFBACAFNgI8IAVBfWwgAmpBf2ohBQwCC0EAIAM2AjxBASAFayACayEFDAELQQAgAiAFQX9zajYCPCADIQULQQAgBTYCSAtBAEEANgJMQQBBADYCQAtBACgCPEEAKAJIIAZBCGoQDEHQhIAIIAZBCGoQFBoLQQAgBkEQajYCBEEACwvmAxIAQQQLBHBsDwEAQQwLBAMAAAAAQRALCAEAAAAAAAAAAEGAhYAICxkCAwUHCw0RExcdHyUpKy81Oz1DR0lPU1lhAEGQ0YAIC1AAAAAAAAAAAP8HAAAAAAAA1fUUAAAAAACxcYIBAAAAAMd9oT8BAAAAO+4/H+oDAADfHDgHUgYAAMHIslJGbQIAwciyUkZtAgD/////AAAAAABB4NGACAsKAgMFBwsNERMXAABB8NGACAsKID0gKDJ0ICsgAABBgNKACAsKID0gKDJ0IC0gAABBkNKACAsGID0gMnQAAEGg0oAICxQgPSA0ICh0PHN1cD4yPC9zdXA+AABBwNKACAsVID0gMiAoMnQ8c3VwPjI8L3N1cD4AAEHg0oAICwU8YnI+AABB8NKACAsbU1ctTkU6IDR0PHN1cD4yPC9zdXA+ICsgNHQAAEGQ04AICxtOVy1TRTogNHQ8c3VwPjI8L3N1cD4gKyAydAAAQbDTgAgLG1NXLU5FOiA0dDxzdXA+Mjwvc3VwPiAtIDR0AABB0NOACAsbTlctU0U6IDR0PHN1cD4yPC9zdXA+IC0gMnQAAEHw04AICxZTVy1ORTogNHQ8c3VwPjI8L3N1cD4AAEGQ1IAICxFOVy1TRTogNHReMiArIDJ0AA==";
var initializer = [3,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,7,0,0,0,0,0,0,213,245,20,0,0,0,0,0,177,113,130,1,0,0,0,0,199,125,161,63,1,0,0,0,59,238,63,31,234,3,0,0,223,28,56,7,82,6,0,0,193,200,178,82,70,109,2,0,193,200,178,82,70,109,2,0,255,255,255,255,0,0,0,0,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,2,3,5,7,11,13,17,19,23,0,32,61,32,40,50,116,32,43,32,0,32,61,32,40,50,116,32,45,32,0,32,61,32,50,116,0,32,61,32,52,32,40,116,60,115,117,112,62,50,60,47,115,117,112,62,0,32,61,32,50,32,40,50,116,60,115,117,112,62,50,60,47,115,117,112,62,0,60,98,114,62,0,83,87,45,78,69,58,32,52,116,60,115,117,112,62,50,60,47,115,117,112,62,32,43,32,52,116,0,78,87,45,83,69,58,32,52,116,60,115,117,112,62,50,60,47,115,117,112,62,32,43,32,50,116,0,83,87,45,78,69,58,32,52,116,60,115,117,112,62,50,60,47,115,117,112,62,32,45,32,52,116,0,78,87,45,83,69,58,32,52,116,60,115,117,112,62,50,60,47,115,117,112,62,32,45,32,50,116,0,83,87,45,78,69,58,32,52,116,60,115,117,112,62,50,60,47,115,117,112,62,0,78,87,45,83,69,58,32,52,116,94,50,32,43,32,50,116,0];
var myAsmJs = (function(global, env, buffer) {
 "use asm";
 var a = new global.Int8Array(buffer);
 var c = new global.Int32Array(buffer);
 var l = env.STACKTOP | 0;
 var D = global.Math.floor;
 var F = global.Math.sqrt;
 var R = global.Math.imul;
 var _ = env._showInfo;
 function ta(b, d, e) {
  b = b | 0;
  d = d | 0;
  e = e | 0;
  var f = 0, g = 0, h = 0, i = 0, j = 0, k = 0, m = 0, n = 0, o = 0, p = 0, q = 0.0, r = 0.0, s = 0.0;
  p = l;
  l = l + 16 | 0;
  o = p;
  f = 10109 + (qa(10109) | 0) | 0;
  pa(f, b) | 0;
  b = f + (qa(f) | 0) | 0;
  f = c[e >> 2] | 0;
  c[o >> 2] = f;
  m = e + 4 | 0;
  g = c[m >> 2] | 0;
  n = o + 4 | 0;
  c[n >> 2] = g;
  if (g | f) {
   h = b + 1 | 0;
   a[b >> 0] = 32;
   b = h + 1 | 0;
   if (!(g & 1073741824)) {
    a[h >> 0] = 43;
    a[b >> 0] = 32;
   } else {
    a[h >> 0] = 45;
    a[b >> 0] = 32;
    k = 0 - f | 0;
    f = k & 2147483647;
    c[o >> 2] = f;
    g = (k >> 31) - g & 2147483647;
    c[n >> 2] = g;
   }
   b = sa(b + 1 | 0, o) | 0;
  }
  do if (f | d | g) {
   j = (ka(d, e) | 0) == 0;
   k = c[m >> 2] | 0;
   if (!j) {
    q = (+(g | 0) * 2147483647.0 + +(f | 0)) * 16.0;
    s = +(R(d, d) | 0);
    r = +(0 - d | 0);
    q = +(~~(+F(+(s + ((k & 1073741824 | 0) == 0 ? -q : q))) + .5) | 0);
    f = ~~((r + q) * .25);
    g = ~~((r - q) * .25);
    b = b + (qa(b) | 0) | 0;
    do if ((f | 0) <= 0) if ((f | 0) < 0) {
     i = b;
     j = 145;
     m = i + 10 | 0;
     do {
      a[i >> 0] = a[j >> 0] | 0;
      i = i + 1 | 0;
      j = j + 1 | 0;
     } while ((i | 0) < (m | 0));
     b = ra(b + (qa(b) | 0) | 0, 0 - f | 0) | 0;
     a[b >> 0] = 41;
     b = b + 1 | 0;
     break;
    } else {
     a[b >> 0] = a[155] | 0;
     a[b + 1 >> 0] = a[156] | 0;
     a[b + 2 >> 0] = a[157] | 0;
     a[b + 3 >> 0] = a[158] | 0;
     a[b + 4 >> 0] = a[159] | 0;
     a[b + 5 >> 0] = a[160] | 0;
     b = b + (qa(b) | 0) | 0;
     break;
    } else {
     i = b;
     j = 135;
     m = i + 10 | 0;
     do {
      a[i >> 0] = a[j >> 0] | 0;
      i = i + 1 | 0;
      j = j + 1 | 0;
     } while ((i | 0) < (m | 0));
     b = ra(b + (qa(b) | 0) | 0, f) | 0;
     a[b >> 0] = 41;
     b = b + 1 | 0;
    } while (0);
    if ((g | 0) > 0) {
     o = b;
     d = o;
     a[d >> 0] = 32;
     a[d + 1 >> 0] = 40;
     a[d + 2 >> 0] = 50;
     a[d + 3 >> 0] = 116;
     o = o + 4 | 0;
     a[o >> 0] = 32;
     a[o + 1 >> 0] = 43;
     a[o + 2 >> 0] = 32;
     a[o + 3 >> 0] = 0;
     b = ra(b + (qa(b) | 0) | 0, g) | 0;
     a[b >> 0] = 41;
     b = b + 1 | 0;
     break;
    }
    if ((g | 0) < 0) {
     o = b;
     d = o;
     a[d >> 0] = 32;
     a[d + 1 >> 0] = 40;
     a[d + 2 >> 0] = 50;
     a[d + 3 >> 0] = 116;
     o = o + 4 | 0;
     a[o >> 0] = 32;
     a[o + 1 >> 0] = 45;
     a[o + 2 >> 0] = 32;
     a[o + 3 >> 0] = 0;
     b = ra(b + (qa(b) | 0) | 0, 0 - g | 0) | 0;
     a[b >> 0] = 41;
     b = b + 1 | 0;
     break;
    } else {
     a[b >> 0] = 32;
     a[b + 1 >> 0] = 50;
     a[b + 2 >> 0] = 116;
     a[b + 3 >> 0] = 0;
     b = b + (qa(b) | 0) | 0;
     break;
    }
   }
   h = c[e >> 2] | 0;
   c[o >> 2] = h;
   c[n >> 2] = k;
   if (h & 1 | 0) {
    f = 0;
    g = 1;
    while (1) {
     j = a[100 + f >> 0] | 0;
     o = (d | 0) % (j | 0) | 0;
     i = (g | 0) == 0;
     if (!(c[356 + (f * 388 | 0) + ((((((R(o, o) | 0) - ((((((h | 0) % (j | 0) | 0) + (R(2147483648 % (j >>> 0) | 0, (k | 0) % (j | 0) | 0) | 0) | 0) >>> 0) % (j >>> 0) | 0) << 4) | 0) % (j | 0) | 0) + j | 0) % (j | 0) | 0) << 2) >> 2] | 0)) {
      a[b >> 0] = i ? 44 : 32;
      a[b + 1 >> 0] = i ? 32 : 40;
      g = 0;
      b = ra(b + 2 | 0, j) | 0;
     }
     f = f + 1 | 0;
     if ((f | 0) == 25) break;
     k = c[m >> 2] | 0;
     h = c[e >> 2] | 0;
    }
    if (g | 0) break;
    a[b >> 0] = 41;
    a[b + 1 >> 0] = 0;
    b = b + 1 | 0;
    break;
   }
   if (!((h | d) & 3)) {
    i = b;
    j = 161;
    m = i + 20 | 0;
    do {
     a[i >> 0] = a[j >> 0] | 0;
     i = i + 1 | 0;
     j = j + 1 | 0;
    } while ((i | 0) < (m | 0));
    f = 4;
    g = 2;
    j = 3;
    i = 29;
   } else {
    i = b;
    j = 181;
    m = i + 21 | 0;
    do {
     a[i >> 0] = a[j >> 0] | 0;
     i = i + 1 | 0;
     j = j + 1 | 0;
    } while ((i | 0) < (m | 0));
    f = 2;
    g = 1;
    j = 2;
    i = 30;
   }
   f = (d | 0) / (f | 0) | 0;
   i = (k << i | h >> g) & 2147483647;
   c[o >> 2] = i;
   h = k << 1 >> j;
   c[n >> 2] = h;
   b = b + (qa(b) | 0) | 0;
   if (f) {
    if ((f | 0) < 0) {
     a[b >> 0] = 32;
     a[b + 1 >> 0] = 45;
     a[b + 2 >> 0] = 32;
     a[b + 3 >> 0] = 0;
     f = 0 - f | 0;
    } else {
     a[b >> 0] = 32;
     a[b + 1 >> 0] = 43;
     a[b + 2 >> 0] = 32;
     a[b + 3 >> 0] = 0;
    }
    b = b + (qa(b) | 0) | 0;
    if ((f | 0) != 1) b = ra(b, f) | 0;
    a[b >> 0] = 116;
    a[b + 1 >> 0] = 0;
    b = b + 1 | 0;
   }
   f = b + 1 | 0;
   a[b >> 0] = 32;
   g = b + 2 | 0;
   if (!(h & 1073741824)) {
    a[f >> 0] = 43;
    a[g >> 0] = 32;
   } else {
    a[f >> 0] = 45;
    a[g >> 0] = 32;
    d = 0 - i | 0;
    c[o >> 2] = d & 2147483647;
    c[n >> 2] = (d >> 31) - (c[n >> 2] | 0) & 2147483647;
   }
   b = sa(b + 3 | 0, o) | 0;
   b = b + (qa(b) | 0) | 0;
   a[b >> 0] = 41;
   a[b + 1 >> 0] = 0;
   b = b + 1 | 0;
  } while (0);
  a[b >> 0] = a[202] | 0;
  a[b + 1 >> 0] = a[203] | 0;
  a[b + 2 >> 0] = a[204] | 0;
  a[b + 3 >> 0] = a[205] | 0;
  a[b + 4 >> 0] = a[206] | 0;
  l = p;
  return;
 }
 function ia(b) {
  b = b | 0;
  var d = 0, e = 0, f = 0, g = 0, h = 0, i = 0, j = 0, k = 0, m = 0, n = 0, o = 0, p = 0, q = 0, r = 0, s = 0, t = 0, u = 0, v = 0, w = 0, x = 0, y = 0, z = 0, A = 0;
  y = l;
  l = l + 32 | 0;
  t = y + 16 | 0;
  u = y + 8 | 0;
  v = y;
  w = c[b >> 2] | 0;
  c[2514] = w;
  s = c[b + 4 >> 2] | 0;
  c[2515] = s;
  e = (s | 0) == 0;
  a : do if (e) {
   switch (w | 0) {
   case 1:
    {
     b = 0;
     break a;
    }
   case 2:
    break;
   default:
    {
     x = 4;
     break a;
    }
   }
   b = 1;
  } else x = 4; while (0);
  b : do if ((x | 0) == 4) if (!(w & 1)) b = 0; else {
   b = 1;
   do {
    d = a[100 + b >> 0] | 0;
    if (e) {
     if ((w | 0) == (d | 0)) {
      b = 1;
      break b;
     }
     if (!((w >>> 0) % (d >>> 0) | 0)) {
      b = 0;
      break b;
     }
    } else if (!((((R(2147483648 % (d >>> 0) | 0, (s >>> 0) % (d >>> 0) | 0) | 0) + ((w >>> 0) % (d >>> 0) | 0) | 0) >>> 0) % (d >>> 0) | 0)) {
     b = 0;
     break b;
    }
    b = b + 1 | 0;
   } while (b >>> 0 < 25);
   ha();
   c[t >> 2] = c[2517];
   r = t + 4 | 0;
   c[r >> 2] = c[2518];
   q = w & 2147483646;
   m = (q | 0) == 0;
   p = m ? 31 : 0;
   q = m ? s : q;
   m = (q & 65535 | 0) == 0;
   p = m ? p + 16 | 0 : p;
   q = m ? q >>> 16 : q;
   m = (q & 255 | 0) == 0;
   p = m ? p + 8 | 0 : p;
   q = m ? q >>> 8 : q;
   m = (q & 15 | 0) == 0;
   p = m ? p + 4 | 0 : p;
   q = m ? q >>> 4 : q;
   m = (q & 3 | 0) == 0;
   p = ((m ? q >>> 2 : q) & 1 ^ 1) + (m ? p + 2 | 0 : p) | 0;
   m = e ? 0 : 31;
   q = (e ^ 1) & 1;
   k = e ? w : s;
   j = k >>> 0 > 65535;
   m = j ? m + 16 | 0 : m;
   k = j ? k >>> 16 : k;
   j = (k & 65280 | 0) == 0;
   m = j ? m : m + 8 | 0;
   k = j ? k : k >>> 8;
   j = (k & 240 | 0) == 0;
   m = j ? m : m + 4 | 0;
   k = j ? k : k >>> 4;
   j = (k & 12 | 0) == 0;
   m = ((j ? k : k >>> 2) >>> 1 & 1) + (j ? m : m + 2 | 0) | 0;
   j = 1 << ((m | 0) % 31 | 0);
   k = u + 4 | 0;
   h = m + -1 | 0;
   m = (m | 0) > (p | 0);
   n = v + 4 | 0;
   o = p + -1 | 0;
   d = 1;
   g = 0;
   i = 0;
   while (1) {
    b = c[20 + ((g | 1) << 2) >> 2] | 0;
    if ((b | 0) >= (s | 0)) {
     if ((b | 0) != (s | 0)) {
      b = 1;
      break b;
     }
     if ((c[20 + (g << 2) >> 2] | 0) >= (w | 0)) {
      b = 1;
      break b;
     }
    }
    b = a[125 + i >> 0] | 0;
    do {
     ga(t, 10068, t);
     d = d + 1 | 0;
    } while (d >>> 0 < b >>> 0);
    e = c[t >> 2] | 0;
    c[u >> 2] = e;
    c[k >> 2] = c[r >> 2];
    if (m) {
     b = q;
     e = h;
     f = j;
     while (1) {
      z = f >>> 1;
      A = (z | 0) == 0;
      b = (A << 31 >> 31) + b | 0;
      f = A ? 1073741824 : z;
      ca(u, u, u);
      if (c[10056 + (b << 2) >> 2] & f | 0) ca(u, t, u);
      if ((e | 0) <= (p | 0)) break; else e = e + -1 | 0;
     }
     b = o;
     e = c[u >> 2] | 0;
    } else b = h;
    if (!((e | 0) == (c[2517] | 0) ? (c[k >> 2] | 0) == (c[2518] | 0) : 0)) x = 23;
    c : do if ((x | 0) == 23 ? (x = 0, ga(u, 10068, v), c[v >> 2] | c[n >> 2] | 0) : 0) {
     if ((b | 0) <= -1) {
      b = 0;
      break b;
     }
     while (1) {
      ca(u, u, u);
      if ((c[u >> 2] | 0) == (c[2517] | 0) ? (c[k >> 2] | 0) == (c[2518] | 0) : 0) {
       b = 0;
       break b;
      }
      ga(u, 10068, v);
      if (!(c[v >> 2] | c[n >> 2])) break c;
      if ((b | 0) > 0) b = b + -1 | 0; else {
       b = 0;
       break b;
      }
     }
    } while (0);
    g = g + 2 | 0;
    i = i + 1 | 0;
   }
  } while (0);
  l = y;
  return b | 0;
 }
 function na(a, b) {
  a = a | 0;
  b = b | 0;
  var d = 0, e = 0, f = 0, g = 0, h = 0, i = 0, j = 0, k = 0, m = 0, n = 0, o = 0, p = 0, q = 0;
  q = l;
  l = l + 32 | 0;
  g = q + 24 | 0;
  d = q + 16 | 0;
  k = q + 8 | 0;
  i = q;
  la(a, b, g);
  j = (c[2520] | 0) == 0 ? -16777216 : -65536;
  p = c[2] | 0;
  o = (a - (c[2522] | 0) << p) + ((c[2521] | 0) / 2 | 0) - (c[2523] | 0) | 0;
  p = ((c[2524] | 0) / 2 | 0) - (b - (c[2525] | 0) << p) + (c[2526] | 0) | 0;
  n = c[g >> 2] | 0;
  if (!(((c[g + 4 >> 2] | 0) != 0 | (n | 0) != 2) & (n & 1 | 0) == 0)) if (!(ia(g) | 0)) {
   e = 0 - b | 0;
   do if (!((a | 0) > (b | 0) & (a | 0) > (e | 0))) if ((a | 0) < (b | 0) & (a | 0) < (e | 0)) {
    f = 0 - a | 0;
    break;
   } else {
    f = (b | 0) > 0 ? b : e;
    break;
   } else f = a; while (0);
   h = f << 1;
   ja(h, h, i);
   fa(g, i, i);
   e = (a | 0) >= (b | 0);
   do if ((b + a | 0) > -1) if (e) {
    ma(i, R(f, -4) | 0, d);
    ma(i, 0 - h | 0, k);
    e = 2;
    f = 4;
    break;
   } else {
    ma(i, f << 2, d);
    ma(i, h, k);
    e = -2;
    f = -4;
    break;
   } else {
    c[d >> 2] = c[i >> 2];
    c[d + 4 >> 2] = c[i + 4 >> 2];
    if (e) {
     ma(i, 0 - h | 0, k);
     e = 2;
     f = 0;
     break;
    } else {
     ma(i, h, k);
     e = -2;
     f = 0;
     break;
    }
   } while (0);
   if (!(ka(f, d) | 0)) {
    h = (ka(e, k) | 0) == 0;
    h = h ? -16777216 : j;
   } else h = j;
  } else h = -16728064; else h = j;
  m = (o | 0) > 0 ? o : 0;
  j = (p | 0) > 0 ? p : 0;
  d = c[2] | 0;
  k = 1 << d;
  n = k + o | 0;
  i = c[2521] | 0;
  n = (n | 0) > (i | 0) ? i : n;
  k = k + p | 0;
  i = c[2524] | 0;
  k = (k | 0) > (i | 0) ? i : k;
  i = (j | 0) < (k | 0);
  if (i) {
   g = (m | 0) < (n | 0);
   d = j;
   do {
    if (g) {
     e = m;
     f = 262144 + (d << 11 << 2) + (m << 2) | 0;
     while (1) {
      c[f >> 2] = h;
      e = e + 1 | 0;
      if ((e | 0) >= (n | 0)) break; else f = f + 4 | 0;
     }
    }
    d = d + 1 | 0;
   } while ((d | 0) < (k | 0));
   d = c[2] | 0;
  }
  do if ((d | 0) > 1) {
   f = (a | 0) > 0 ? a : 0 - a | 0;
   d = (b | 0) > 0;
   e = 0 - b | 0;
   g = d ? b : e;
   if ((f | 0) < (g | 0)) {
    if (d & (b + -1 | 0) == (a | 0)) break;
   } else {
    if (((b | 0) > -1 | (a | 0) != (e | 0)) & (o | 0) > -1 & (o | 0) < (c[2521] | 0) & i) {
     e = j;
     d = 262144 + (j << 11 << 2) + (o << 2) | 0;
     while (1) {
      c[d >> 2] = -4144960;
      e = e + 1 | 0;
      if ((e | 0) >= (k | 0)) break; else d = d + 8192 | 0;
     }
    }
    if (!((b | 0) < 1 & (f | 0) == (g | 0))) break;
   }
   d = (1 << c[2]) + p | 0;
   if ((d | 0) <= (c[2524] | 0) & (d | 0) > 0 & (m | 0) < (n | 0)) {
    e = m;
    d = 262144 + ((d << 11) + -2048 << 2) + (m << 2) | 0;
    while (1) {
     c[d >> 2] = -4144960;
     e = e + 1 | 0;
     if ((e | 0) >= (n | 0)) break; else d = d + 4 | 0;
    }
   }
  } while (0);
  l = q;
  return;
 }
 function wa(b, d, e, f) {
  b = b | 0;
  d = d | 0;
  e = e | 0;
  f = f | 0;
  var g = 0, h = 0, i = 0, j = 0, k = 0, m = 0, n = 0, o = 0;
  n = l;
  l = l + 16 | 0;
  j = n + 8 | 0;
  m = n;
  c[2521] = e;
  c[2524] = f;
  i = j + 4 | 0;
  c[i >> 2] = 0;
  c[j >> 2] = 0;
  h = 0;
  f = 0;
  e = 0;
  while (1) {
   g = a[b >> 0] | 0;
   if (!(g << 24 >> 24)) break;
   o = (g << 24 >> 24) + -48 | 0;
   g = (f * 10 | 0) + o & 2147483647;
   c[j >> 2] = g;
   e = ~~((+(o | 0) + +(f | 0) * 10.0) * 4.656612873077393e-10) + (e * 10 | 0) | 0;
   c[i >> 2] = e;
   h = h + 1 | 0;
   if ((h | 0) >= 19) {
    f = g;
    break;
   } else {
    b = b + 1 | 0;
    f = g;
   }
  }
  a : do switch (d | 0) {
  case 1:
   {
    fa(j, 12, j);
    c[m >> 2] = 1;
    c[m + 4 >> 2] = 0;
    ea(j, m, j);
    e = c[i >> 2] | 0;
    f = c[j >> 2] | 0;
    if ((e | 0) > 0 | (f | 0) > 0) {
     e = (~~+F(+(+(e | 0) * 2147483648.0 + +(f | 0) + -1.0)) + 1 | 0) / 2 | 0;
     b = 0 - e | 0;
     o = f - (R(e << 2, e) | 0) | 0;
     f = o & 2147483647;
     f = (o & 1073741824 | 0) == 0 ? f : f + -2147483647 | 0;
     do if ((f | 0) >= ((R(e, -2) | 0) + 2 | 0)) {
      if ((f | 0) < 1) {
       c[2522] = b;
       e = 1 - e - f | 0;
       break;
      }
      if ((f | 0) > (e << 1 | 0)) {
       c[2522] = e;
       e = (R(e, -3) | 0) + -1 + f | 0;
       break;
      } else {
       c[2522] = f + ~e;
       e = b;
       break;
      }
     } else c[2522] = (R(e, -3) | 0) + 1 - f; while (0);
     c[2525] = e;
    }
    c[2523] = 0;
    c[2526] = 0;
    k = 22;
    break;
   }
  case 2:
   {
    c[3] = f;
    c[4] = e;
    k = 22;
    break;
   }
  default:
   {
    e = c[2] | 0;
    if ((d | 0) == 3) {
     if ((e | 0) == 5) break a;
     c[2] = e + 1;
     c[2523] = c[2523] << 1;
     e = c[2526] << 1;
    } else {
     if (!e) break a;
     c[2] = e + -1;
     c[2523] = c[2523] >> 1;
     e = c[2526] >> 1;
    }
    c[2526] = e;
    k = 22;
   }
  } while (0);
  if ((k | 0) == 22) {
   la(c[2522] | 0, c[2525] | 0, m);
   sa(10609, m) | 0;
  }
  l = n;
  return 0;
 }
 function ua(b, d) {
  b = b | 0;
  d = d | 0;
  var e = 0, f = 0, g = 0, h = 0, i = 0, j = 0, k = 0;
  k = l;
  l = l + 32 | 0;
  h = k + 16 | 0;
  i = k + 8 | 0;
  j = k;
  f = c[2] | 0;
  g = ((c[2523] | 0) + b + ((c[2521] | 0) / -2 | 0) >> f) + (c[2522] | 0) | 0;
  f = (c[2525] | 0) + 1 + ((c[2526] | 0) - d + ((c[2524] | 0) / 2 | 0) >> f) | 0;
  la(g, f, h);
  b = 0 - f | 0;
  do if (!((g | 0) > (f | 0) & (g | 0) > (b | 0))) if ((g | 0) < (f | 0) & (g | 0) < (b | 0)) {
   b = 0 - g | 0;
   break;
  } else {
   b = (f | 0) > 0 ? f : b;
   break;
  } else b = g; while (0);
  a[10109] = 0;
  d = b << 1;
  ja(d, d, i);
  fa(h, i, i);
  e = (g | 0) >= (f | 0);
  do if ((f + g | 0) > -1) if (e) {
   ma(i, R(b, -4) | 0, j);
   ta(207, 4, j);
   ma(i, 0 - d | 0, j);
   ta(234, 2, j);
   break;
  } else {
   ma(i, b << 2, j);
   ta(261, -4, j);
   ma(i, d, j);
   ta(288, -2, j);
   break;
  } else {
   ta(315, 0, i);
   if (e) {
    ma(i, 0 - d | 0, j);
    ta(337, 2, j);
    break;
   } else {
    ma(i, d, j);
    ta(288, -2, j);
    break;
   }
  } while (0);
  j = 10109 + (qa(10109) | 0) | 0;
  a[j >> 0] = 120;
  a[j + 1 >> 0] = 61;
  j = ra(j + 2 | 0, g) | 0;
  a[j >> 0] = 44;
  a[j + 1 >> 0] = 32;
  a[j + 2 >> 0] = 121;
  a[j + 3 >> 0] = 61;
  j = ra(j + 4 | 0, f) | 0;
  a[j >> 0] = 44;
  a[j + 1 >> 0] = 32;
  a[j + 2 >> 0] = 110;
  a[j + 3 >> 0] = 61;
  a[j + 4 >> 0] = 60;
  a[j + 5 >> 0] = 98;
  a[j + 6 >> 0] = 62;
  j = sa(j + 7 | 0, h) | 0;
  a[j >> 0] = 60;
  a[j + 1 >> 0] = 47;
  a[j + 2 >> 0] = 98;
  a[j + 3 >> 0] = 62;
  a[j + 4 >> 0] = 44;
  a[j + 5 >> 0] = 32;
  a[j + 6 >> 0] = 116;
  a[j + 7 >> 0] = 61;
  ra(j + 8 | 0, b) | 0;
  la(c[2522] | 0, c[2525] | 0, h);
  sa(10609, h) | 0;
  _(10109, 10609);
  l = k;
  return;
 }
 function ca(a, b, d) {
  a = a | 0;
  b = b | 0;
  d = d | 0;
  var e = 0, f = 0, g = 0, h = 0, i = 0, j = 0.0, k = 0.0, l = 0.0, m = 0.0, n = 0.0, o = 0, p = 0, q = 0.0, r = 0.0;
  g = c[2515] | 0;
  e = c[a >> 2] | 0;
  f = c[b >> 2] | 0;
  h = c[2514] | 0;
  if (!g) {
   da(e, f, d, h);
   a = 0;
  } else {
   o = c[b + 4 >> 2] | 0;
   j = +(e | 0);
   p = R(f, e) | 0;
   q = +(f | 0);
   b = c[2516] | 0;
   p = (R(p, b) | 0) & 2147483647;
   l = +(p | 0);
   n = +(h | 0);
   r = +D(+((j * q + n * l) * 4.656612873077393e-10 + .5));
   p = (~~r >>> 0) + (R(o, e) | 0) + (R(p, g) | 0) & 2147483647;
   k = +(g | 0);
   m = +(o | 0);
   i = ~~((r + (j * m + k * l) + (p >>> 0 < 1073741824 ? 536870912.0 : -536870912.0)) * 4.656612873077393e-10) >>> 0;
   e = c[a + 4 >> 2] | 0;
   l = +(e | 0);
   b = (R(p + (R(e, f) | 0) | 0, b) | 0) & 2147483647;
   j = +(b | 0);
   n = +D(+((q * l + +(p | 0) + n * j) * 4.656612873077393e-10 + .5));
   b = (~~n >>> 0) + (R(e, o) | 0) + (R(b, g) | 0) + i | 0;
   e = b & 2147483647;
   a = ~~((n + (m * l + k * j + +(i >>> 0)) + (e >>> 0 < 1073741824 ? 536870912.0 : -536870912.0)) * 4.656612873077393e-10) >>> 0;
   if (a >>> 0 <= g >>> 0 ? e >>> 0 < h >>> 0 | (a | 0) != (g | 0) : 0) b = e; else {
    b = b - h & 2147483647;
    a = (e - h >> 31) - g + a & 2147483647;
   }
   c[d >> 2] = b;
  }
  c[d + 4 >> 2] = a;
  return;
 }
 function ba(a) {
  a = a | 0;
  var b = 0, d = 0, e = 0.0, f = 0, g = 0, h = 0, i = 0, j = 0.0, k = 0;
  f = c[2514] | 0;
  k = a + 8 | 0;
  d = c[a >> 2] | 0;
  h = ~~+D(+((+(c[k >> 2] | 0) * 2147483648.0 + +(c[a + 4 >> 2] | 0) + +(d | 0) * 4.656612873077393e-10) / (+(c[2515] | 0) + +(f | 0) * 4.656612873077393e-10) + .5)) >>> 0;
  h = (h | 0) < 0 ? 2147483647 : h;
  j = +(h | 0);
  i = 0;
  b = 0;
  e = 0.0;
  while (1) {
   g = d + b - (R(f, h) | 0) & 2147483647;
   e = e + (+(b | 0) + (+(d | 0) - j * +(f | 0)));
   d = e < 0.0;
   b = ~~+D(+(((g >>> 0 < 1073741824 ? 536870912.0 : -536870912.0) + (d ? e + 4611686018427388000.0 : e)) * 4.656612873077393e-10));
   c[a + (i << 2) >> 2] = g;
   g = i + 1 | 0;
   if ((g | 0) == 2) break;
   i = g;
   e = d ? -2147483648.0 : 0.0;
   f = c[10056 + (g << 2) >> 2] | 0;
   d = c[a + (g << 2) >> 2] | 0;
  }
  i = (c[k >> 2] | 0) + b & 2147483647;
  c[k >> 2] = i;
  if (i | 0) {
   b = 0;
   d = 0;
   while (1) {
    i = a + (d << 2) | 0;
    b = (c[i >> 2] | 0) + b + (c[10056 + (d << 2) >> 2] | 0) | 0;
    c[i >> 2] = b & 2147483647;
    d = d + 1 | 0;
    if ((d | 0) == 2) break; else b = b >>> 31;
   }
   c[k >> 2] = 0;
  }
  return;
 }
 function ka(a, b) {
  a = a | 0;
  b = b | 0;
  var d = 0, e = 0.0, f = 0, g = 0, h = 0, i = 0, j = 0, k = 0, m = 0, n = 0.0, o = 0.0;
  k = l;
  l = l + 16 | 0;
  h = k;
  d = c[b >> 2] | 0;
  c[h >> 2] = d;
  f = c[b + 4 >> 2] | 0;
  j = h + 4 | 0;
  c[j >> 2] = f;
  g = (f & 1073741824 | 0) == 0;
  if (!g) {
   m = 0 - d | 0;
   d = m & 2147483647;
   c[h >> 2] = d;
   f = (m >> 31) - f & 2147483647;
   c[j >> 2] = f;
  }
  e = (+(f | 0) * 2147483647.0 + +(d | 0)) * 16.0;
  n = +(R(a, a) | 0);
  e = n + (g ? -e : e);
  if (!(e < 0.0) ? (o = +(0 - a | 0), n = +(~~(+F(+e) + .5) | 0), m = ~~((o + n) * .25), i = ~~((o - n) * .25), ja((m << 1) + a | 0, m, h), ea(h, b, h), ea(h, b, h), (c[j >> 2] | c[h >> 2] | 0) == 0) : 0) {
   ja((i << 1) + a | 0, i, h);
   ea(h, b, h);
   ea(h, b, h);
   d = (c[j >> 2] | c[h >> 2] | 0) == 0 & 1;
  } else d = 0;
  l = k;
  return d | 0;
 }
 function sa(b, d) {
  b = b | 0;
  d = d | 0;
  var e = 0, f = 0, g = 0, h = 0.0;
  f = 0;
  g = c[d + 4 >> 2] | 0;
  d = c[d >> 2] | 0;
  e = b + 19 | 0;
  while (1) {
   h = +(d | 0) + +((g | 0) % 10 | 0 | 0) * 2147483648.0;
   d = ~~(h / 10.0);
   e = e + -1 | 0;
   a[e >> 0] = ~~(h - +(d * 10 | 0)) + 48;
   f = f + 1 | 0;
   if ((f | 0) == 19) {
    d = 0;
    break;
   } else g = (g | 0) / 10 | 0;
  }
  while (1) {
   if ((a[b + d >> 0] | 0) != 48) {
    f = d;
    g = 4;
    break;
   }
   d = d + 1 | 0;
   if ((d | 0) >= 18) {
    g = 3;
    break;
   }
  }
  if ((g | 0) == 3) if ((d | 0) == 18) {
   f = 18;
   g = 4;
  } else e = d;
  if ((g | 0) == 4) {
   e = 0 - f | 0;
   d = f;
   do {
    g = b + d | 0;
    a[g + e >> 0] = a[g >> 0] | 0;
    d = d + 1 | 0;
   } while ((d | 0) != 19);
   e = 19;
   d = f;
  }
  b = b + (e - d) | 0;
  a[b >> 0] = 0;
  return b | 0;
 }
 function la(a, b, d) {
  a = a | 0;
  b = b | 0;
  d = d | 0;
  var e = 0, f = 0, g = 0, h = 0, i = 0;
  i = l;
  l = l + 16 | 0;
  h = i;
  f = (a | 0) < (b | 0);
  g = 0 - b | 0;
  do if ((a | 0) < (g | 0) | ((a | 0) < 0 | f)) {
   if ((b | 0) > -1 & f ? (e = 0 - a | 0, (b | 0) > (e | 0)) : 0) {
    ja((b << 2) + -3 | 0, b, d);
    a = e;
    break;
   }
   if ((a | 0) > (g | 0) | ((a | 0) > 0 | (a | 0) > (b | 0))) {
    ja((b << 2) + -1 | 0, b, d);
    break;
   } else {
    ja(a << 2 | 1, a, d);
    a = g;
    break;
   }
  } else {
   ja(a << 2 | 3, a, d);
   a = b;
  } while (0);
  c[h >> 2] = a & 2147483647;
  c[h + 4 >> 2] = a >> 31 & 2147483647;
  ea(d, h, d);
  ea(d, 12, d);
  l = i;
  return;
 }
 function oa(b, d, e, f) {
  b = b | 0;
  d = d | 0;
  e = e | 0;
  f = f | 0;
  var g = 0, h = 0, i = 0, j = 0;
  if (!(a[10108] | 0)) aa();
  h = c[2522] | 0;
  j = c[2523] | 0;
  i = c[2] | 0;
  b = (j + b >> i) + h | 0;
  h = (j + d >> i) + h | 0;
  j = c[2525] | 0;
  d = 0 - (c[2526] | 0) | 0;
  g = j - (d - e >> i) | 0;
  e = j - (d - f >> i) | 0;
  if ((b | 0) <= (h | 0)) {
   f = (g | 0) > (e | 0);
   d = b;
   while (1) {
    if (!f) {
     b = g;
     while (1) {
      na(d, b);
      if ((b | 0) < (e | 0)) b = b + 1 | 0; else break;
     }
    }
    if ((d | 0) < (h | 0)) d = d + 1 | 0; else break;
   }
  }
  return;
 }
 function ra(b, c) {
  b = b | 0;
  c = c | 0;
  var d = 0, e = 0, f = 0;
  if ((c | 0) < 0) {
   a[b >> 0] = 45;
   e = 0;
   b = b + 1 | 0;
   f = 1e9;
   c = 0 - c | 0;
  } else {
   e = 0;
   f = 1e9;
  }
  while (1) {
   d = (c | 0) / (f | 0) | 0;
   if (!(d | e)) d = e; else {
    c = c - (R(d, f) | 0) | 0;
    a[b >> 0] = d + 48;
    d = 1;
    b = b + 1 | 0;
   }
   if ((f | 0) > 19) {
    e = d;
    f = (f | 0) / 10 | 0;
   } else break;
  }
  f = b + 1 | 0;
  a[b >> 0] = c + 48;
  a[f >> 0] = 0;
  return f | 0;
 }
 function ga(a, b, d) {
  a = a | 0;
  b = b | 0;
  d = d | 0;
  var e = 0, f = 0, g = 0, h = 0;
  f = c[2514] | 0;
  g = c[2515] | 0;
  e = (c[b >> 2] | 0) + (c[a >> 2] | 0) | 0;
  h = e & 2147483647;
  a = (e >>> 31) + (c[a + 4 >> 2] | 0) + (c[b + 4 >> 2] | 0) | 0;
  if (a >>> 0 <= g >>> 0 ? (h | 0) < (f | 0) | (a | 0) != (g | 0) : 0) b = h; else {
   b = e - f & 2147483647;
   a = a - g + (h - f >> 31) | 0;
  }
  c[d >> 2] = b;
  c[d + 4 >> 2] = a & 2147483647;
  return;
 }
 function ha() {
  var a = 0, b = 0;
  c[2518] = 0;
  if (!(c[2515] | 0)) c[2517] = 1; else {
   b = c[2514] | 0;
   a = R(2 - (R(b, b) | 0) | 0, b) | 0;
   a = R(2 - (R(a, b) | 0) | 0, a) | 0;
   a = R(2 - (R(a, b) | 0) | 0, a) | 0;
   c[2516] = (R(2 - (R(a, b) | 0) | 0, 0 - a | 0) | 0) & 2147483647;
   c[2519] = 1;
   c[2517] = 0;
   ba(10068);
  }
  return;
 }
 function aa() {
  var b = 0, d = 0, e = 0;
  d = 0;
  do {
   e = a[100 + d >> 0] | 0;
   b = ((e | 0) / 2 | 0) + 1 | 0;
   while (1) {
    c[356 + (d * 388 | 0) + (((R(b, b) | 0) % (e | 0) | 0) << 2) >> 2] = 1;
    if ((b | 0) > 0) b = b + -1 | 0; else break;
   }
   d = d + 1 | 0;
  } while ((d | 0) != 25);
  a[10108] = 1;
  return;
 }
 function pa(b, c) {
  b = b | 0;
  c = c | 0;
  var d = 0, e = 0, f = 0;
  d = a[c >> 0] | 0;
  if (!(d << 24 >> 24)) c = b; else {
   e = c;
   f = b;
   while (1) {
    e = e + 1 | 0;
    c = f + 1 | 0;
    a[f >> 0] = d;
    d = a[e >> 0] | 0;
    if (!(d << 24 >> 24)) break; else f = c;
   }
  }
  a[c >> 0] = 0;
  return b | 0;
 }
 function da(a, b, d, e) {
  a = a | 0;
  b = b | 0;
  d = d | 0;
  e = e | 0;
  var f = 0;
  f = R(b, a) | 0;
  if ((e | 0) < 32768) a = (f | 0) % (e | 0) | 0; else {
   a = f - (R(~~+D(+(+(a | 0) * +(b | 0) / +(e | 0) + .5)), e) | 0) | 0;
   a = ((a | 0) < 0 ? e : 0) + a | 0;
  }
  c[d >> 2] = a;
  return;
 }
 function va(a, b) {
  a = a | 0;
  b = b | 0;
  var d = 0, e = 0;
  e = (c[2523] | 0) - a | 0;
  d = c[2] | 0;
  c[2522] = (c[2522] | 0) + (e >> d);
  a = (1 << d) + -1 | 0;
  c[2523] = e & a;
  b = (c[2526] | 0) + b | 0;
  c[2525] = (c[2525] | 0) + (b >> d);
  c[2526] = b & a;
  return;
 }
 function ja(a, b, d) {
  a = a | 0;
  b = b | 0;
  d = d | 0;
  var e = 0;
  e = (R(b, a) | 0) & 2147483647;
  c[d >> 2] = e;
  c[d + 4 >> 2] = ~~((+(a | 0) * +(b | 0) + (e >>> 0 < 1073741824 ? 536870912.0 : -536870912.0)) * 4.656612873077393e-10) >>> 0;
  return;
 }
 function ma(a, b, d) {
  a = a | 0;
  b = b | 0;
  d = d | 0;
  var e = 0, f = 0;
  f = l;
  l = l + 16 | 0;
  e = f;
  c[e + 4 >> 2] = 0;
  if ((b | 0) > -1) {
   c[e >> 2] = b;
   ea(a, e, d);
  } else {
   c[e >> 2] = 0 - b;
   fa(a, e, d);
  }
  l = f;
  return;
 }
 function ea(a, b, d) {
  a = a | 0;
  b = b | 0;
  d = d | 0;
  var e = 0;
  e = (c[b >> 2] | 0) + (c[a >> 2] | 0) | 0;
  c[d >> 2] = e & 2147483647;
  c[d + 4 >> 2] = (e >>> 31) + (c[a + 4 >> 2] | 0) + (c[b + 4 >> 2] | 0) & 2147483647;
  return;
 }
 function fa(a, b, d) {
  a = a | 0;
  b = b | 0;
  d = d | 0;
  var e = 0;
  e = (c[a >> 2] | 0) - (c[b >> 2] | 0) | 0;
  c[d >> 2] = e & 2147483647;
  c[d + 4 >> 2] = (e >> 31) + (c[a + 4 >> 2] | 0) - (c[b + 4 >> 2] | 0) & 2147483647;
  return;
 }
 function qa(b) {
  b = b | 0;
  var c = 0;
  c = b;
  while (1) if (!(a[c >> 0] | 0)) break; else c = c + 1 | 0;
  return c - b | 0;
 }
 return {
  _drawPartialUlamSpiral: oa,
  _moveSpiral: va,
  _nbrChanged: wa,
  _ShowInformation: ua
 };
});

function get(x)
{
  return document.getElementById(x);
}

function PtrToString(ptr)
{
  var t=-1;
  var i = 0;
  var str="", outString="";
  do
  {
    for (i=0; i<1024; i++)
    {
      t = HEAP8[((ptr++)>>0)];
      if (t==0)
      {
        break;
      }
      if (t>=128)
      {
        t = ((t-192)<<6) + HEAP8[((ptr++)>>0)] - 128;
      }
      str += String.fromCharCode(t);
    }
    outString += str;
    str = "";
  } while (t!=0);
  outString += str;
  return outString;
}

function getHeight()
{
  return Math.min(canvas.scrollHeight, canvas.height);
}

function getWidth()
{
  return Math.min(canvas.scrollWidth, canvas.width);
}

function moveSpiral(deltaX, deltaY)
{      
  var ctx = canvas.getContext("2d");
  var width = getWidth();
  var height = getHeight();
  asm["_moveSpiral"](deltaX, deltaY);
  if (deltaX >= 0)
  {
    if (deltaY >= 0)
    {    // Move to right and bottom.
      if (width-deltaX > 0 && height-deltaY > 0)
      {  // Width and height must be greater than zero to avoid exception.
        ctx.drawImage(ctx.canvas, 0, 0,                          // Topmost pixel of source.
                      width-deltaX, height-deltaY,               // Width and height of source.
                      deltaX, deltaY,                            // Topmost pixel of destination.
                      width-deltaX, height-deltaY);              // Width and height of destination.
        drawSpiral(ctx, 0, 0, width, deltaY);                    // Draw new points at top of graphic.
        drawSpiral(ctx, 0, deltaY, deltaX, height-deltaY);       // Draw new points at left of graphic.
      }
    }
    else
    {    // Move to right and up.
      if (width-deltaX > 0 && height+deltaY > 0)
      {  // Width and height must be greater than zero to avoid exception.
        ctx.drawImage(ctx.canvas, 0, -deltaY,                    // Topmost pixel of source.
                      width-deltaX, height+deltaY,               // Width and height of source.
                      deltaX, 0,                                 // Topmost pixel of destination.
                      width-deltaX, height+deltaY);              // Width and height of destination.
        drawSpiral(ctx, 0, height+deltaY, width, -deltaY);       // Draw new points at bottom of graphic.
        drawSpiral(ctx, 0, 0, deltaX, height+deltaY);            // Draw new points at left of graphic.
      }
    }
  }
  else if (deltaY >= 0)
  {      // Move to left and bottom.
    if (width+deltaX > 0 && height-deltaY > 0)
    {    // Width and height must be greater than zero to avoid exception.
      ctx.drawImage(ctx.canvas, -deltaX, 0,                      // Topmost pixel of source.
                    width+deltaX, height-deltaY,                 // Width and height of source.
                    0, deltaY,                                   // Topmost pixel of destination.
                    width+deltaX, height-deltaY);                // Width and height of destination.
      drawSpiral(ctx, 0, 0, width, deltaY);                      // Draw new points at top of graphic.
      drawSpiral(ctx, width+deltaX, deltaY, -deltaX, height-deltaY); // Draw new points at right of graphic.
    }
  }
  else
  {      // Move to left and up.
    if (width+deltaX > 0 && height+deltaY > 0)
    {    // Width and height must be greater than zero to avoid exception.
      ctx.drawImage(ctx.canvas, -deltaX, -deltaY,                // Topmost pixel of source.
                    width+deltaX, height+deltaY,                 // Width and height of source.
                    0, 0,                                        // Topmost pixel of destination.
                    width+deltaX, height+deltaY);                // Width and height of destination.
      drawSpiral(ctx, 0, height+deltaY, width, -deltaY);         // Draw new points at bottom of graphic.
      drawSpiral(ctx, width+deltaX, 0, -deltaX, height+deltaY);  // Draw new points at right of graphic.
    }
  }
}

function drawSpiral(ctx, left, top, width, height)
{
  if (width != 0 && height != 0)
  {
    var rowNbr, leftPixelSrc, leftPixelDest;
    var startX = left - (getWidth() >> 1);
    var startY = top - (getHeight() >> 1);
    asm["_drawPartialUlamSpiral"](startX, startX+width, -(startY+height), -startY);
    if (!asmjs)
    {         // Using WebAssembly: copy from WebAssembly buffer to Canvas double buffer.
      leftPixelSrc = top*8192+left*4;
      leftPixelDest = (top+32)*8192+left*4;
      for (rowNbr=0; rowNbr<height; rowNbr++)
      {
        bitsCanvas.set(pixels.subarray(leftPixelSrc, leftPixelSrc + 4*width), leftPixelDest);
        leftPixelSrc += 8192;
        leftPixelDest += 8192;
      }
    }
    ctx.putImageData(imgData, 0, -32, left, 32+top, width, height);
  }
}

function updateSpiral(input, nbr)
{
  var idx;
  var value = input.value;
  if (input != 0)
  {
    for (idx=0; idx<value.length; idx++)  
    {
      HEAP8[11000000+idx] = value.charCodeAt(idx);
    }
    HEAP8[11000000+idx] = 0;
  }
  var width = getWidth();
  var height = getHeight();
  asm["_nbrChanged"](11000000, nbr, width, height);
  drawSpiral(canvas.getContext("2d"), 0, 0, width, height);
}

function charDecode(ch)
{
  if (ch >= 65 && ch <= 90)
  {                            // Character between A and Z.
    ch -= 65;                  // Convert to range 0 to 25.
  } 
  else if (ch >= 97 && ch <= 122)
  {                            // Character between a and z.
    ch -= 71;                  // Convert to range 26 to 51.
  }
  else if (ch >= 48 && ch <= 57)
  {                            // Character between 0 and 9.
    ch += 4;                   // Convert to range 52 to 61.
  }
  else if (ch == 43)
  {                            // Character is a plus sign.
    ch = 62;                   // Convert to code 62.
  }
  else if (ch == 47)
  {                            // Character is a slash.
    ch = 63;                   // Convert to code 63.
  }
  return ch;
}

function b64decode(str, out)
{
  var ch;
  var idxDest, idxSrc;
  var blocks,left_over;
  var len = str.length;
  // Ignore 
  if (str.charAt(len-1) == '=')
  {
    len--;
  }
  if (str.charAt(len-1) == '=')
  {
    len--;
  }
  blocks = len & -4;
  for (idxDest=0,idxSrc=0; idxSrc < blocks; idxDest += 3,idxSrc += 4)
  {
    out[idxDest] = (charDecode(str.charCodeAt(idxSrc)) << 2) + ((charDecode(str.charCodeAt(idxSrc+1)) & 0x30) >> 4);
    out[idxDest+1] = (charDecode(str.charCodeAt(idxSrc+1)) << 4) + (charDecode(str.charCodeAt(idxSrc+2)) >> 2);
    out[idxDest+2] = (charDecode(str.charCodeAt(idxSrc+2)) << 6) + charDecode(str.charCodeAt(idxSrc+3));
  }
  left_over = len & 3;
  if (left_over == 2)
  {
    out[idxDest] = (charDecode(str.charCodeAt(idxSrc)) << 2) + ((charDecode(str.charCodeAt(idxSrc+1)) & 0x30) >> 4);
    out[idxDest+1] = (charDecode(str.charCodeAt(idxSrc+1)) << 4);
  }
  else if (left_over == 3)
  {
    out[idxDest] = (charDecode(str.charCodeAt(idxSrc)) << 2) + ((charDecode(str.charCodeAt(idxSrc+1)) & 0x30) >> 4);
    out[idxDest+1] = (charDecode(str.charCodeAt(idxSrc+1)) << 4) + (charDecode(str.charCodeAt(idxSrc+2)) >> 2);
    out[idxDest+2] = charDecode(str.charCodeAt(idxSrc+2)) << 6;
  }
}

function showInfo(bottomText, centerText)
{
  var bottom = PtrToString(bottomText);
  var centerValue = PtrToString(centerText);
  if (centerValue != center.value)
  {
    center.value = centerValue;
  } 
  info.innerHTML = bottom;
}

function startLowLevelCode()
{
  var length, bytes;
  var info;
  imgData = canvas.getContext("2d").createImageData(2048, 4096);  // 32 MB;
  buffer = imgData.data.buffer;          // Reserve 16 MB.
  if (asmjs)
  {                                      // Asm.js initialization.
    HEAP8 = new Uint8Array(buffer);
    HEAP8.fill(0);                       // Initialize entire array to zero.
    HEAP8.set(initializer, 8);           // Initialized data starts from offset 8.
    global = {"Math": Math, "Int8Array": Int8Array, "Int32Array": Int32Array};
    env = {"STACKTOP": 12000000, "STACKMAX": 13000000,
      abortStackOverflow: function(q) {},
      _showInfo: showInfo};
    // check for imul support, and also for correctness ( https://bugs.webkit.org/show_bug.cgi?id=126345 )
    if (!Math['imul'] || Math['imul'](0xffffffff, 5) !== -5) Math['imul'] = function imul(a, b)
    {
      var ah  = a >>> 16;
      var al = a & 0xffff;
      var bh  = b >>> 16;
      var bl = b & 0xffff;
      return (al*bl + ((ah*bl + al*bh) << 16))|0;
    };
    Math.imul = Math['imul'];
    asm = myAsmJs(global, env, buffer);  // Link asm.js module.
    ShowInformation = asm["_ShowInformation"];
  }
  else
  {                                      // WebAssembly initialization.
    length = wasm.length * 3 / 4;
    if (wasm.charCodeAt(wasm.length - 1) == 61)
    {                                    // Base64 ending equal sign found.
      length--;
    }
    if (wasm.charCodeAt(wasm.length - 2) == 61)
    {                                    // Another base64 ending equal sign found.
      length--;
    }
    bytes = new Int8Array(length);
    // Decode Base64.
    b64decode(wasm, bytes);
    info = {"env": {"_showInfo": showInfo}};
    WebAssembly["instantiate"](bytes, info).then(function(results)
    {
      asm = results["instance"]["exports"];
      ShowInformation = asm["_ShowInformation"];
      HEAP8 = new Uint8Array(asm["memory"]["buffer"]);
      bitsCanvas = new Uint8Array(buffer);
      pixels = HEAP8.subarray(asm["_getPixels"]());
      updateSpiral(center, 1);
      return;
    });
  }
}

function checkStart()
{
  return (center.value.length < start.value.length || 
        (center.value.length == start.value.length && center.value < start.value));
}

function zoomIn()
{
  if (zoom < 32)
  {
    zoom <<= 1;
    if (zoom == 32)
    {
      zoomin.disabled = true;
    }
    zoomout.disabled = false;
    updateSpiral(0, 3);
  }
}

function zoomOut()
{
  if (zoom > 1)
  {
    zoom >>= 1;
    if (zoom == 1)
    {
      zoomout.disabled = true;
    }
    zoomin.disabled = false;
    updateSpiral(0, 4);
  }
}

function startUp()
{  
  canvas = get("canvas");
  zoomin = get("zoomin");
  zoomout = get("zoomout");
  center = get("center");
  start = get("start");
  zoom = 8;
  zoomDone = 0;
  isMouseDown = false;
  var domRect = canvas.getBoundingClientRect();
  canvas.width = domRect.width;
  canvas.height = domRect.height;
  startLowLevelCode();
  zoomin.onclick = function ()
  {
    zoomIn();
  };
  zoomout.onclick = function ()
  {
    zoomOut();
  };
  canvas.onkeydown = function (e)
  {
    if (checkStart())
    {    // Cannot show spiral when center is less than start value.
      return;
    }
    var evt = e || window.event;
    var key = evt.keyCode;
    switch (key)
    {
      case 37: // Left arrow:
        moveSpiral(4, 0);
        ShowInformation(-1, -1);
        evt.preventDefault();          // Do not propagate this key.
        break; 
      case 38: // Up arrow:
        moveSpiral(0, 4);
        ShowInformation(-1, -1);
        evt.preventDefault();          // Do not propagate this key.
        break; 
      case 39: // Right arrow:
        moveSpiral(-4, 0);
        ShowInformation(-1, -1);
        evt.preventDefault();          // Do not propagate this key.
        break; 
      case 40: // Down arrow:
        moveSpiral(0, -4);
        ShowInformation(-1, -1);
        evt.preventDefault();          // Do not propagate this key.
        break; 
    }      
  };
  canvas.onmousemove = function(e)
  {
    if (checkStart())
    {    // Cannot show spiral when center is less than start value.
      return;
    }
    var evt = e || window.event;
    var newX = evt.clientX;
    var newY = evt.clientY;      // Coordinates relative to window.
    var rect = canvas.getBoundingClientRect();
    newX -= rect.left;
    newY -= rect.top;            // Now coordinates are relative to canvas.
    if (isMouseDown)
    {
      if (newX != currentX || newY != currentY)
      {
        moveSpiral(newX - currentX, newY - currentY);
        currentX = newX;
        currentY = newY;
      }
    } 
    else
    {
      if (newX < canvas.width && newY < canvas.height)
      {
        asm["_ShowInformation"](newX, newY);
      }
    }
  };  
  canvas.onmousedown = function(e)
  {
    var evt = e || window.event;
    currentX = evt.clientX;
    currentY = evt.clientY;      // Coordinates relative to window. 
    var rect = canvas.getBoundingClientRect();
    currentX -= rect.left;
    currentY -= rect.top;        // Now coordinates are relative to canvas.
    isMouseDown = true;
  };
  document.onmouseup = function()
  {
    isMouseDown = false;
  };
  canvas.addEventListener("touchstart", function(e)
  {
    var evt = e || window.event;
    var touches = evt.targetTouches;
    touch = touches[0];
    prevX1stTouch = Math.round(touch.pageX);
    prevY1stTouch = Math.round(touch.pageY);
    if (touches.length == 2)
    {
      touch = touches[1];
      prevX2ndTouch = Math.round(touch.pageX);
      prevY2ndTouch = Math.round(touch.pageY);
      zoomDone = 0;
    }    
  }, false);  
  canvas.addEventListener("touchmove", function(e)
  {
    var touch2, oldDist, newDist, diffX, diffY;
    var evt = e || window.event;
    var touches = evt.targetTouches;
    var touch1 = touches[0];
	var newX = Math.round(touch1.pageX);
	var newY = Math.round(touch1.pageY);
    if (touches.length == 1)
    {      // Drag gesture.
      if (newX != prevX1stTouch || newY != prevY1stTouch)
      {
        moveSpiral(newX - prevX1stTouch, newY - prevY1stTouch);
        prevX1stTouch = newX;
        prevY1stTouch = newY;
        ShowInformation(-1, -1);
      }      
    }
    else if (touches.length == 2 && !zoomDone)
    {      // Pinch (zoom in and zoom out) gesture.
      touch2 = evt.touches[1];
           // Get square of distance between fingers.
      diffX = prevX2ndTouch - prevX1stTouch;
      diffY = prevY2ndTouch - prevY1stTouch;
      oldDist = diffX * diffX + diffY * diffY;
      diffX = Math.round(touch2.pageX) - newX;
      diffY = Math.round(touch2.pageY) - newY;
      newDist = diffX * diffX + diffY * diffY;
      if (newDist > oldDist)
      {    // Zoom in.
        zoomIn();
        zoomDone = 1;
      }
      if (newDist < oldDist)
      {    // Zoom out.
        zoomOut();
        zoomDone = 1;
      }
    }
  }, false);
  center.onkeydown = function(e)
  {
    var evt = e || window.event;
    var key = evt.keyCode;
    if (evt.ctrlKey == false && evt.altKey == false && evt.metaKey == false)
    {                                    // No modifier key pressed.
      if (key != 8 && key != 9 && key != 37 && key != 39 && key != 45 && key != 46)
      {                                  // Not backspace, tab, right or left arrow, insert or delete key.
        if (key >= 0x60 && key <= 0x69)
        {
          key -= 0x30;                   // Convert numpad key to standard digit key.
        }
        if (key < 0x30 || key > 0x39 || center.value.length >= 18)
        {                                // Key is not a digit or number is too large.
          evt.preventDefault();          // Do not propagate this key.
        }
      }
    }
  };
  center.oninput = function()
  {
    var ctx;
    if (checkStart())
    {
      get("info").innerHTML = get("cannotShow").innerHTML;
      ctx = canvas.getContext("2d");
      ctx.beginPath();
      ctx.rect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "black";
      ctx.fill();
    }
    else
    {
      get("info").innerHTML = "";
      updateSpiral(center, 1);
    }
  };
  start.onkeydown = function(e)
  {
    var evt = e || window.event;
    var key = evt.keyCode;
    if (evt.ctrlKey == false && evt.altKey == false && evt.metaKey == false)
    {                                    // No modifier key pressed.
      if (key != 8 && key != 9 && key != 37 && key != 39 && key != 45 && key != 46)
      {                                  // Not backspace, tab, right or left arrow, insert or delete key.
        if (key >= 0x60 && key <= 0x69)
        {
          key -= 0x30;                   // Convert numpad key to standard digit key.
        }
        if (key < 0x30 || key > 0x39 || start.value.length >= 18)
        {                                // Key is not a digit or number is too large.
          evt.preventDefault();          // Do not propagate this key.
        }
      }
    }
  };
  start.oninput = function()
  {
    ShowInformation(-1, -1);
    updateSpiral(start, 2);
  };
  window.onresize = function()
  {
    var domRect = canvas.getBoundingClientRect();
    canvas.width = domRect.width;
    canvas.height = domRect.height;
    updateSpiral(center, 1);
  };
  if (asmjs)
  {
    updateSpiral(center, 1);
  }
}

addEventListener("load", startUp);
})(this);
