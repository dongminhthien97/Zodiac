(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const i of document.querySelectorAll('link[rel="modulepreload"]'))r(i);new MutationObserver(i=>{for(const l of i)if(l.type==="childList")for(const o of l.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&r(o)}).observe(document,{childList:!0,subtree:!0});function n(i){const l={};return i.integrity&&(l.integrity=i.integrity),i.referrerPolicy&&(l.referrerPolicy=i.referrerPolicy),i.crossOrigin==="use-credentials"?l.credentials="include":i.crossOrigin==="anonymous"?l.credentials="omit":l.credentials="same-origin",l}function r(i){if(i.ep)return;i.ep=!0;const l=n(i);fetch(i.href,l)}})();function fu(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}var pu={exports:{}},Oi={},mu={exports:{}},L={};/**
 * @license React
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var yr=Symbol.for("react.element"),nf=Symbol.for("react.portal"),rf=Symbol.for("react.fragment"),lf=Symbol.for("react.strict_mode"),of=Symbol.for("react.profiler"),sf=Symbol.for("react.provider"),af=Symbol.for("react.context"),uf=Symbol.for("react.forward_ref"),cf=Symbol.for("react.suspense"),df=Symbol.for("react.memo"),ff=Symbol.for("react.lazy"),zs=Symbol.iterator;function pf(e){return e===null||typeof e!="object"?null:(e=zs&&e[zs]||e["@@iterator"],typeof e=="function"?e:null)}var hu={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},gu=Object.assign,yu={};function _n(e,t,n){this.props=e,this.context=t,this.refs=yu,this.updater=n||hu}_n.prototype.isReactComponent={};_n.prototype.setState=function(e,t){if(typeof e!="object"&&typeof e!="function"&&e!=null)throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,e,t,"setState")};_n.prototype.forceUpdate=function(e){this.updater.enqueueForceUpdate(this,e,"forceUpdate")};function vu(){}vu.prototype=_n.prototype;function zo(e,t,n){this.props=e,this.context=t,this.refs=yu,this.updater=n||hu}var Oo=zo.prototype=new vu;Oo.constructor=zo;gu(Oo,_n.prototype);Oo.isPureReactComponent=!0;var Os=Array.isArray,xu=Object.prototype.hasOwnProperty,Lo={current:null},wu={key:!0,ref:!0,__self:!0,__source:!0};function Su(e,t,n){var r,i={},l=null,o=null;if(t!=null)for(r in t.ref!==void 0&&(o=t.ref),t.key!==void 0&&(l=""+t.key),t)xu.call(t,r)&&!wu.hasOwnProperty(r)&&(i[r]=t[r]);var s=arguments.length-2;if(s===1)i.children=n;else if(1<s){for(var a=Array(s),c=0;c<s;c++)a[c]=arguments[c+2];i.children=a}if(e&&e.defaultProps)for(r in s=e.defaultProps,s)i[r]===void 0&&(i[r]=s[r]);return{$$typeof:yr,type:e,key:l,ref:o,props:i,_owner:Lo.current}}function mf(e,t){return{$$typeof:yr,type:e.type,key:t,ref:e.ref,props:e.props,_owner:e._owner}}function Ao(e){return typeof e=="object"&&e!==null&&e.$$typeof===yr}function hf(e){var t={"=":"=0",":":"=2"};return"$"+e.replace(/[=:]/g,function(n){return t[n]})}var Ls=/\/+/g;function nl(e,t){return typeof e=="object"&&e!==null&&e.key!=null?hf(""+e.key):t.toString(36)}function Qr(e,t,n,r,i){var l=typeof e;(l==="undefined"||l==="boolean")&&(e=null);var o=!1;if(e===null)o=!0;else switch(l){case"string":case"number":o=!0;break;case"object":switch(e.$$typeof){case yr:case nf:o=!0}}if(o)return o=e,i=i(o),e=r===""?"."+nl(o,0):r,Os(i)?(n="",e!=null&&(n=e.replace(Ls,"$&/")+"/"),Qr(i,t,n,"",function(c){return c})):i!=null&&(Ao(i)&&(i=mf(i,n+(!i.key||o&&o.key===i.key?"":(""+i.key).replace(Ls,"$&/")+"/")+e)),t.push(i)),1;if(o=0,r=r===""?".":r+":",Os(e))for(var s=0;s<e.length;s++){l=e[s];var a=r+nl(l,s);o+=Qr(l,t,n,a,i)}else if(a=pf(e),typeof a=="function")for(e=a.call(e),s=0;!(l=e.next()).done;)l=l.value,a=r+nl(l,s++),o+=Qr(l,t,n,a,i);else if(l==="object")throw t=String(e),Error("Objects are not valid as a React child (found: "+(t==="[object Object]"?"object with keys {"+Object.keys(e).join(", ")+"}":t)+"). If you meant to render a collection of children, use an array instead.");return o}function Tr(e,t,n){if(e==null)return e;var r=[],i=0;return Qr(e,r,"","",function(l){return t.call(n,l,i++)}),r}function gf(e){if(e._status===-1){var t=e._result;t=t(),t.then(function(n){(e._status===0||e._status===-1)&&(e._status=1,e._result=n)},function(n){(e._status===0||e._status===-1)&&(e._status=2,e._result=n)}),e._status===-1&&(e._status=0,e._result=t)}if(e._status===1)return e._result.default;throw e._result}var fe={current:null},Gr={transition:null},yf={ReactCurrentDispatcher:fe,ReactCurrentBatchConfig:Gr,ReactCurrentOwner:Lo};function ku(){throw Error("act(...) is not supported in production builds of React.")}L.Children={map:Tr,forEach:function(e,t,n){Tr(e,function(){t.apply(this,arguments)},n)},count:function(e){var t=0;return Tr(e,function(){t++}),t},toArray:function(e){return Tr(e,function(t){return t})||[]},only:function(e){if(!Ao(e))throw Error("React.Children.only expected to receive a single React element child.");return e}};L.Component=_n;L.Fragment=rf;L.Profiler=of;L.PureComponent=zo;L.StrictMode=lf;L.Suspense=cf;L.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=yf;L.act=ku;L.cloneElement=function(e,t,n){if(e==null)throw Error("React.cloneElement(...): The argument must be a React element, but you passed "+e+".");var r=gu({},e.props),i=e.key,l=e.ref,o=e._owner;if(t!=null){if(t.ref!==void 0&&(l=t.ref,o=Lo.current),t.key!==void 0&&(i=""+t.key),e.type&&e.type.defaultProps)var s=e.type.defaultProps;for(a in t)xu.call(t,a)&&!wu.hasOwnProperty(a)&&(r[a]=t[a]===void 0&&s!==void 0?s[a]:t[a])}var a=arguments.length-2;if(a===1)r.children=n;else if(1<a){s=Array(a);for(var c=0;c<a;c++)s[c]=arguments[c+2];r.children=s}return{$$typeof:yr,type:e.type,key:i,ref:l,props:r,_owner:o}};L.createContext=function(e){return e={$$typeof:af,_currentValue:e,_currentValue2:e,_threadCount:0,Provider:null,Consumer:null,_defaultValue:null,_globalName:null},e.Provider={$$typeof:sf,_context:e},e.Consumer=e};L.createElement=Su;L.createFactory=function(e){var t=Su.bind(null,e);return t.type=e,t};L.createRef=function(){return{current:null}};L.forwardRef=function(e){return{$$typeof:uf,render:e}};L.isValidElement=Ao;L.lazy=function(e){return{$$typeof:ff,_payload:{_status:-1,_result:e},_init:gf}};L.memo=function(e,t){return{$$typeof:df,type:e,compare:t===void 0?null:t}};L.startTransition=function(e){var t=Gr.transition;Gr.transition={};try{e()}finally{Gr.transition=t}};L.unstable_act=ku;L.useCallback=function(e,t){return fe.current.useCallback(e,t)};L.useContext=function(e){return fe.current.useContext(e)};L.useDebugValue=function(){};L.useDeferredValue=function(e){return fe.current.useDeferredValue(e)};L.useEffect=function(e,t){return fe.current.useEffect(e,t)};L.useId=function(){return fe.current.useId()};L.useImperativeHandle=function(e,t,n){return fe.current.useImperativeHandle(e,t,n)};L.useInsertionEffect=function(e,t){return fe.current.useInsertionEffect(e,t)};L.useLayoutEffect=function(e,t){return fe.current.useLayoutEffect(e,t)};L.useMemo=function(e,t){return fe.current.useMemo(e,t)};L.useReducer=function(e,t,n){return fe.current.useReducer(e,t,n)};L.useRef=function(e){return fe.current.useRef(e)};L.useState=function(e){return fe.current.useState(e)};L.useSyncExternalStore=function(e,t,n){return fe.current.useSyncExternalStore(e,t,n)};L.useTransition=function(){return fe.current.useTransition()};L.version="18.3.1";mu.exports=L;var je=mu.exports;const Eu=fu(je);/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var vf=je,xf=Symbol.for("react.element"),wf=Symbol.for("react.fragment"),Sf=Object.prototype.hasOwnProperty,kf=vf.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,Ef={key:!0,ref:!0,__self:!0,__source:!0};function Nu(e,t,n){var r,i={},l=null,o=null;n!==void 0&&(l=""+n),t.key!==void 0&&(l=""+t.key),t.ref!==void 0&&(o=t.ref);for(r in t)Sf.call(t,r)&&!Ef.hasOwnProperty(r)&&(i[r]=t[r]);if(e&&e.defaultProps)for(r in t=e.defaultProps,t)i[r]===void 0&&(i[r]=t[r]);return{$$typeof:xf,type:e,key:l,ref:o,props:i,_owner:kf.current}}Oi.Fragment=wf;Oi.jsx=Nu;Oi.jsxs=Nu;pu.exports=Oi;var u=pu.exports,zl={},ju={exports:{}},Re={},Cu={exports:{}},_u={};/**
 * @license React
 * scheduler.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */(function(e){function t(j,P){var z=j.length;j.push(P);e:for(;0<z;){var M=z-1>>>1,U=j[M];if(0<i(U,P))j[M]=P,j[z]=U,z=M;else break e}}function n(j){return j.length===0?null:j[0]}function r(j){if(j.length===0)return null;var P=j[0],z=j.pop();if(z!==P){j[0]=z;e:for(var M=0,U=j.length,ct=U>>>1;M<ct;){var be=2*(M+1)-1,Yt=j[be],Pt=be+1,Rr=j[Pt];if(0>i(Yt,z))Pt<U&&0>i(Rr,Yt)?(j[M]=Rr,j[Pt]=z,M=Pt):(j[M]=Yt,j[be]=z,M=be);else if(Pt<U&&0>i(Rr,z))j[M]=Rr,j[Pt]=z,M=Pt;else break e}}return P}function i(j,P){var z=j.sortIndex-P.sortIndex;return z!==0?z:j.id-P.id}if(typeof performance=="object"&&typeof performance.now=="function"){var l=performance;e.unstable_now=function(){return l.now()}}else{var o=Date,s=o.now();e.unstable_now=function(){return o.now()-s}}var a=[],c=[],f=1,d=null,h=3,w=!1,m=!1,v=!1,k=typeof setTimeout=="function"?setTimeout:null,g=typeof clearTimeout=="function"?clearTimeout:null,p=typeof setImmediate<"u"?setImmediate:null;typeof navigator<"u"&&navigator.scheduling!==void 0&&navigator.scheduling.isInputPending!==void 0&&navigator.scheduling.isInputPending.bind(navigator.scheduling);function y(j){for(var P=n(c);P!==null;){if(P.callback===null)r(c);else if(P.startTime<=j)r(c),P.sortIndex=P.expirationTime,t(a,P);else break;P=n(c)}}function S(j){if(v=!1,y(j),!m)if(n(a)!==null)m=!0,he(N);else{var P=n(c);P!==null&&qt(S,P.startTime-j)}}function N(j,P){m=!1,v&&(v=!1,g(T),T=-1),w=!0;var z=h;try{for(y(P),d=n(a);d!==null&&(!(d.expirationTime>P)||j&&!me());){var M=d.callback;if(typeof M=="function"){d.callback=null,h=d.priorityLevel;var U=M(d.expirationTime<=P);P=e.unstable_now(),typeof U=="function"?d.callback=U:d===n(a)&&r(a),y(P)}else r(a);d=n(a)}if(d!==null)var ct=!0;else{var be=n(c);be!==null&&qt(S,be.startTime-P),ct=!1}return ct}finally{d=null,h=z,w=!1}}var R=!1,C=null,T=-1,I=5,O=-1;function me(){return!(e.unstable_now()-O<I)}function Ke(){if(C!==null){var j=e.unstable_now();O=j;var P=!0;try{P=C(!0,j)}finally{P?Fe():(R=!1,C=null)}}else R=!1}var Fe;if(typeof p=="function")Fe=function(){p(Ke)};else if(typeof MessageChannel<"u"){var Qe=new MessageChannel,_r=Qe.port2;Qe.port1.onmessage=Ke,Fe=function(){_r.postMessage(null)}}else Fe=function(){k(Ke,0)};function he(j){C=j,R||(R=!0,Fe())}function qt(j,P){T=k(function(){j(e.unstable_now())},P)}e.unstable_IdlePriority=5,e.unstable_ImmediatePriority=1,e.unstable_LowPriority=4,e.unstable_NormalPriority=3,e.unstable_Profiling=null,e.unstable_UserBlockingPriority=2,e.unstable_cancelCallback=function(j){j.callback=null},e.unstable_continueExecution=function(){m||w||(m=!0,he(N))},e.unstable_forceFrameRate=function(j){0>j||125<j?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):I=0<j?Math.floor(1e3/j):5},e.unstable_getCurrentPriorityLevel=function(){return h},e.unstable_getFirstCallbackNode=function(){return n(a)},e.unstable_next=function(j){switch(h){case 1:case 2:case 3:var P=3;break;default:P=h}var z=h;h=P;try{return j()}finally{h=z}},e.unstable_pauseExecution=function(){},e.unstable_requestPaint=function(){},e.unstable_runWithPriority=function(j,P){switch(j){case 1:case 2:case 3:case 4:case 5:break;default:j=3}var z=h;h=j;try{return P()}finally{h=z}},e.unstable_scheduleCallback=function(j,P,z){var M=e.unstable_now();switch(typeof z=="object"&&z!==null?(z=z.delay,z=typeof z=="number"&&0<z?M+z:M):z=M,j){case 1:var U=-1;break;case 2:U=250;break;case 5:U=1073741823;break;case 4:U=1e4;break;default:U=5e3}return U=z+U,j={id:f++,callback:P,priorityLevel:j,startTime:z,expirationTime:U,sortIndex:-1},z>M?(j.sortIndex=z,t(c,j),n(a)===null&&j===n(c)&&(v?(g(T),T=-1):v=!0,qt(S,z-M))):(j.sortIndex=U,t(a,j),m||w||(m=!0,he(N))),j},e.unstable_shouldYield=me,e.unstable_wrapCallback=function(j){var P=h;return function(){var z=h;h=P;try{return j.apply(this,arguments)}finally{h=z}}}})(_u);Cu.exports=_u;var Nf=Cu.exports;/**
 * @license React
 * react-dom.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var jf=je,_e=Nf;function E(e){for(var t="https://reactjs.org/docs/error-decoder.html?invariant="+e,n=1;n<arguments.length;n++)t+="&args[]="+encodeURIComponent(arguments[n]);return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}var Ru=new Set,Zn={};function Qt(e,t){yn(e,t),yn(e+"Capture",t)}function yn(e,t){for(Zn[e]=t,e=0;e<t.length;e++)Ru.add(t[e])}var lt=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),Ol=Object.prototype.hasOwnProperty,Cf=/^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/,As={},Ms={};function _f(e){return Ol.call(Ms,e)?!0:Ol.call(As,e)?!1:Cf.test(e)?Ms[e]=!0:(As[e]=!0,!1)}function Rf(e,t,n,r){if(n!==null&&n.type===0)return!1;switch(typeof t){case"function":case"symbol":return!0;case"boolean":return r?!1:n!==null?!n.acceptsBooleans:(e=e.toLowerCase().slice(0,5),e!=="data-"&&e!=="aria-");default:return!1}}function Tf(e,t,n,r){if(t===null||typeof t>"u"||Rf(e,t,n,r))return!0;if(r)return!1;if(n!==null)switch(n.type){case 3:return!t;case 4:return t===!1;case 5:return isNaN(t);case 6:return isNaN(t)||1>t}return!1}function pe(e,t,n,r,i,l,o){this.acceptsBooleans=t===2||t===3||t===4,this.attributeName=r,this.attributeNamespace=i,this.mustUseProperty=n,this.propertyName=e,this.type=t,this.sanitizeURL=l,this.removeEmptyString=o}var re={};"children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e){re[e]=new pe(e,0,!1,e,null,!1,!1)});[["acceptCharset","accept-charset"],["className","class"],["htmlFor","for"],["httpEquiv","http-equiv"]].forEach(function(e){var t=e[0];re[t]=new pe(t,1,!1,e[1],null,!1,!1)});["contentEditable","draggable","spellCheck","value"].forEach(function(e){re[e]=new pe(e,2,!1,e.toLowerCase(),null,!1,!1)});["autoReverse","externalResourcesRequired","focusable","preserveAlpha"].forEach(function(e){re[e]=new pe(e,2,!1,e,null,!1,!1)});"allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e){re[e]=new pe(e,3,!1,e.toLowerCase(),null,!1,!1)});["checked","multiple","muted","selected"].forEach(function(e){re[e]=new pe(e,3,!0,e,null,!1,!1)});["capture","download"].forEach(function(e){re[e]=new pe(e,4,!1,e,null,!1,!1)});["cols","rows","size","span"].forEach(function(e){re[e]=new pe(e,6,!1,e,null,!1,!1)});["rowSpan","start"].forEach(function(e){re[e]=new pe(e,5,!1,e.toLowerCase(),null,!1,!1)});var Mo=/[\-:]([a-z])/g;function Fo(e){return e[1].toUpperCase()}"accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e){var t=e.replace(Mo,Fo);re[t]=new pe(t,1,!1,e,null,!1,!1)});"xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e){var t=e.replace(Mo,Fo);re[t]=new pe(t,1,!1,e,"http://www.w3.org/1999/xlink",!1,!1)});["xml:base","xml:lang","xml:space"].forEach(function(e){var t=e.replace(Mo,Fo);re[t]=new pe(t,1,!1,e,"http://www.w3.org/XML/1998/namespace",!1,!1)});["tabIndex","crossOrigin"].forEach(function(e){re[e]=new pe(e,1,!1,e.toLowerCase(),null,!1,!1)});re.xlinkHref=new pe("xlinkHref",1,!1,"xlink:href","http://www.w3.org/1999/xlink",!0,!1);["src","href","action","formAction"].forEach(function(e){re[e]=new pe(e,1,!1,e.toLowerCase(),null,!0,!0)});function Io(e,t,n,r){var i=re.hasOwnProperty(t)?re[t]:null;(i!==null?i.type!==0:r||!(2<t.length)||t[0]!=="o"&&t[0]!=="O"||t[1]!=="n"&&t[1]!=="N")&&(Tf(t,n,i,r)&&(n=null),r||i===null?_f(t)&&(n===null?e.removeAttribute(t):e.setAttribute(t,""+n)):i.mustUseProperty?e[i.propertyName]=n===null?i.type===3?!1:"":n:(t=i.attributeName,r=i.attributeNamespace,n===null?e.removeAttribute(t):(i=i.type,n=i===3||i===4&&n===!0?"":""+n,r?e.setAttributeNS(r,t,n):e.setAttribute(t,n))))}var ut=jf.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED,br=Symbol.for("react.element"),Jt=Symbol.for("react.portal"),Zt=Symbol.for("react.fragment"),Do=Symbol.for("react.strict_mode"),Ll=Symbol.for("react.profiler"),Tu=Symbol.for("react.provider"),bu=Symbol.for("react.context"),Uo=Symbol.for("react.forward_ref"),Al=Symbol.for("react.suspense"),Ml=Symbol.for("react.suspense_list"),Bo=Symbol.for("react.memo"),ft=Symbol.for("react.lazy"),Pu=Symbol.for("react.offscreen"),Fs=Symbol.iterator;function Pn(e){return e===null||typeof e!="object"?null:(e=Fs&&e[Fs]||e["@@iterator"],typeof e=="function"?e:null)}var K=Object.assign,rl;function Un(e){if(rl===void 0)try{throw Error()}catch(n){var t=n.stack.trim().match(/\n( *(at )?)/);rl=t&&t[1]||""}return`
`+rl+e}var il=!1;function ll(e,t){if(!e||il)return"";il=!0;var n=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{if(t)if(t=function(){throw Error()},Object.defineProperty(t.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(t,[])}catch(c){var r=c}Reflect.construct(e,[],t)}else{try{t.call()}catch(c){r=c}e.call(t.prototype)}else{try{throw Error()}catch(c){r=c}e()}}catch(c){if(c&&r&&typeof c.stack=="string"){for(var i=c.stack.split(`
`),l=r.stack.split(`
`),o=i.length-1,s=l.length-1;1<=o&&0<=s&&i[o]!==l[s];)s--;for(;1<=o&&0<=s;o--,s--)if(i[o]!==l[s]){if(o!==1||s!==1)do if(o--,s--,0>s||i[o]!==l[s]){var a=`
`+i[o].replace(" at new "," at ");return e.displayName&&a.includes("<anonymous>")&&(a=a.replace("<anonymous>",e.displayName)),a}while(1<=o&&0<=s);break}}}finally{il=!1,Error.prepareStackTrace=n}return(e=e?e.displayName||e.name:"")?Un(e):""}function bf(e){switch(e.tag){case 5:return Un(e.type);case 16:return Un("Lazy");case 13:return Un("Suspense");case 19:return Un("SuspenseList");case 0:case 2:case 15:return e=ll(e.type,!1),e;case 11:return e=ll(e.type.render,!1),e;case 1:return e=ll(e.type,!0),e;default:return""}}function Fl(e){if(e==null)return null;if(typeof e=="function")return e.displayName||e.name||null;if(typeof e=="string")return e;switch(e){case Zt:return"Fragment";case Jt:return"Portal";case Ll:return"Profiler";case Do:return"StrictMode";case Al:return"Suspense";case Ml:return"SuspenseList"}if(typeof e=="object")switch(e.$$typeof){case bu:return(e.displayName||"Context")+".Consumer";case Tu:return(e._context.displayName||"Context")+".Provider";case Uo:var t=e.render;return e=e.displayName,e||(e=t.displayName||t.name||"",e=e!==""?"ForwardRef("+e+")":"ForwardRef"),e;case Bo:return t=e.displayName||null,t!==null?t:Fl(e.type)||"Memo";case ft:t=e._payload,e=e._init;try{return Fl(e(t))}catch{}}return null}function Pf(e){var t=e.type;switch(e.tag){case 24:return"Cache";case 9:return(t.displayName||"Context")+".Consumer";case 10:return(t._context.displayName||"Context")+".Provider";case 18:return"DehydratedFragment";case 11:return e=t.render,e=e.displayName||e.name||"",t.displayName||(e!==""?"ForwardRef("+e+")":"ForwardRef");case 7:return"Fragment";case 5:return t;case 4:return"Portal";case 3:return"Root";case 6:return"Text";case 16:return Fl(t);case 8:return t===Do?"StrictMode":"Mode";case 22:return"Offscreen";case 12:return"Profiler";case 21:return"Scope";case 13:return"Suspense";case 19:return"SuspenseList";case 25:return"TracingMarker";case 1:case 0:case 17:case 2:case 14:case 15:if(typeof t=="function")return t.displayName||t.name||null;if(typeof t=="string")return t}return null}function Ct(e){switch(typeof e){case"boolean":case"number":case"string":case"undefined":return e;case"object":return e;default:return""}}function zu(e){var t=e.type;return(e=e.nodeName)&&e.toLowerCase()==="input"&&(t==="checkbox"||t==="radio")}function zf(e){var t=zu(e)?"checked":"value",n=Object.getOwnPropertyDescriptor(e.constructor.prototype,t),r=""+e[t];if(!e.hasOwnProperty(t)&&typeof n<"u"&&typeof n.get=="function"&&typeof n.set=="function"){var i=n.get,l=n.set;return Object.defineProperty(e,t,{configurable:!0,get:function(){return i.call(this)},set:function(o){r=""+o,l.call(this,o)}}),Object.defineProperty(e,t,{enumerable:n.enumerable}),{getValue:function(){return r},setValue:function(o){r=""+o},stopTracking:function(){e._valueTracker=null,delete e[t]}}}}function Pr(e){e._valueTracker||(e._valueTracker=zf(e))}function Ou(e){if(!e)return!1;var t=e._valueTracker;if(!t)return!0;var n=t.getValue(),r="";return e&&(r=zu(e)?e.checked?"true":"false":e.value),e=r,e!==n?(t.setValue(e),!0):!1}function ai(e){if(e=e||(typeof document<"u"?document:void 0),typeof e>"u")return null;try{return e.activeElement||e.body}catch{return e.body}}function Il(e,t){var n=t.checked;return K({},t,{defaultChecked:void 0,defaultValue:void 0,value:void 0,checked:n??e._wrapperState.initialChecked})}function Is(e,t){var n=t.defaultValue==null?"":t.defaultValue,r=t.checked!=null?t.checked:t.defaultChecked;n=Ct(t.value!=null?t.value:n),e._wrapperState={initialChecked:r,initialValue:n,controlled:t.type==="checkbox"||t.type==="radio"?t.checked!=null:t.value!=null}}function Lu(e,t){t=t.checked,t!=null&&Io(e,"checked",t,!1)}function Dl(e,t){Lu(e,t);var n=Ct(t.value),r=t.type;if(n!=null)r==="number"?(n===0&&e.value===""||e.value!=n)&&(e.value=""+n):e.value!==""+n&&(e.value=""+n);else if(r==="submit"||r==="reset"){e.removeAttribute("value");return}t.hasOwnProperty("value")?Ul(e,t.type,n):t.hasOwnProperty("defaultValue")&&Ul(e,t.type,Ct(t.defaultValue)),t.checked==null&&t.defaultChecked!=null&&(e.defaultChecked=!!t.defaultChecked)}function Ds(e,t,n){if(t.hasOwnProperty("value")||t.hasOwnProperty("defaultValue")){var r=t.type;if(!(r!=="submit"&&r!=="reset"||t.value!==void 0&&t.value!==null))return;t=""+e._wrapperState.initialValue,n||t===e.value||(e.value=t),e.defaultValue=t}n=e.name,n!==""&&(e.name=""),e.defaultChecked=!!e._wrapperState.initialChecked,n!==""&&(e.name=n)}function Ul(e,t,n){(t!=="number"||ai(e.ownerDocument)!==e)&&(n==null?e.defaultValue=""+e._wrapperState.initialValue:e.defaultValue!==""+n&&(e.defaultValue=""+n))}var Bn=Array.isArray;function dn(e,t,n,r){if(e=e.options,t){t={};for(var i=0;i<n.length;i++)t["$"+n[i]]=!0;for(n=0;n<e.length;n++)i=t.hasOwnProperty("$"+e[n].value),e[n].selected!==i&&(e[n].selected=i),i&&r&&(e[n].defaultSelected=!0)}else{for(n=""+Ct(n),t=null,i=0;i<e.length;i++){if(e[i].value===n){e[i].selected=!0,r&&(e[i].defaultSelected=!0);return}t!==null||e[i].disabled||(t=e[i])}t!==null&&(t.selected=!0)}}function Bl(e,t){if(t.dangerouslySetInnerHTML!=null)throw Error(E(91));return K({},t,{value:void 0,defaultValue:void 0,children:""+e._wrapperState.initialValue})}function Us(e,t){var n=t.value;if(n==null){if(n=t.children,t=t.defaultValue,n!=null){if(t!=null)throw Error(E(92));if(Bn(n)){if(1<n.length)throw Error(E(93));n=n[0]}t=n}t==null&&(t=""),n=t}e._wrapperState={initialValue:Ct(n)}}function Au(e,t){var n=Ct(t.value),r=Ct(t.defaultValue);n!=null&&(n=""+n,n!==e.value&&(e.value=n),t.defaultValue==null&&e.defaultValue!==n&&(e.defaultValue=n)),r!=null&&(e.defaultValue=""+r)}function Bs(e){var t=e.textContent;t===e._wrapperState.initialValue&&t!==""&&t!==null&&(e.value=t)}function Mu(e){switch(e){case"svg":return"http://www.w3.org/2000/svg";case"math":return"http://www.w3.org/1998/Math/MathML";default:return"http://www.w3.org/1999/xhtml"}}function $l(e,t){return e==null||e==="http://www.w3.org/1999/xhtml"?Mu(t):e==="http://www.w3.org/2000/svg"&&t==="foreignObject"?"http://www.w3.org/1999/xhtml":e}var zr,Fu=function(e){return typeof MSApp<"u"&&MSApp.execUnsafeLocalFunction?function(t,n,r,i){MSApp.execUnsafeLocalFunction(function(){return e(t,n,r,i)})}:e}(function(e,t){if(e.namespaceURI!=="http://www.w3.org/2000/svg"||"innerHTML"in e)e.innerHTML=t;else{for(zr=zr||document.createElement("div"),zr.innerHTML="<svg>"+t.valueOf().toString()+"</svg>",t=zr.firstChild;e.firstChild;)e.removeChild(e.firstChild);for(;t.firstChild;)e.appendChild(t.firstChild)}});function er(e,t){if(t){var n=e.firstChild;if(n&&n===e.lastChild&&n.nodeType===3){n.nodeValue=t;return}}e.textContent=t}var Vn={animationIterationCount:!0,aspectRatio:!0,borderImageOutset:!0,borderImageSlice:!0,borderImageWidth:!0,boxFlex:!0,boxFlexGroup:!0,boxOrdinalGroup:!0,columnCount:!0,columns:!0,flex:!0,flexGrow:!0,flexPositive:!0,flexShrink:!0,flexNegative:!0,flexOrder:!0,gridArea:!0,gridRow:!0,gridRowEnd:!0,gridRowSpan:!0,gridRowStart:!0,gridColumn:!0,gridColumnEnd:!0,gridColumnSpan:!0,gridColumnStart:!0,fontWeight:!0,lineClamp:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,tabSize:!0,widows:!0,zIndex:!0,zoom:!0,fillOpacity:!0,floodOpacity:!0,stopOpacity:!0,strokeDasharray:!0,strokeDashoffset:!0,strokeMiterlimit:!0,strokeOpacity:!0,strokeWidth:!0},Of=["Webkit","ms","Moz","O"];Object.keys(Vn).forEach(function(e){Of.forEach(function(t){t=t+e.charAt(0).toUpperCase()+e.substring(1),Vn[t]=Vn[e]})});function Iu(e,t,n){return t==null||typeof t=="boolean"||t===""?"":n||typeof t!="number"||t===0||Vn.hasOwnProperty(e)&&Vn[e]?(""+t).trim():t+"px"}function Du(e,t){e=e.style;for(var n in t)if(t.hasOwnProperty(n)){var r=n.indexOf("--")===0,i=Iu(n,t[n],r);n==="float"&&(n="cssFloat"),r?e.setProperty(n,i):e[n]=i}}var Lf=K({menuitem:!0},{area:!0,base:!0,br:!0,col:!0,embed:!0,hr:!0,img:!0,input:!0,keygen:!0,link:!0,meta:!0,param:!0,source:!0,track:!0,wbr:!0});function Hl(e,t){if(t){if(Lf[e]&&(t.children!=null||t.dangerouslySetInnerHTML!=null))throw Error(E(137,e));if(t.dangerouslySetInnerHTML!=null){if(t.children!=null)throw Error(E(60));if(typeof t.dangerouslySetInnerHTML!="object"||!("__html"in t.dangerouslySetInnerHTML))throw Error(E(61))}if(t.style!=null&&typeof t.style!="object")throw Error(E(62))}}function Vl(e,t){if(e.indexOf("-")===-1)return typeof t.is=="string";switch(e){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var Wl=null;function $o(e){return e=e.target||e.srcElement||window,e.correspondingUseElement&&(e=e.correspondingUseElement),e.nodeType===3?e.parentNode:e}var Kl=null,fn=null,pn=null;function $s(e){if(e=wr(e)){if(typeof Kl!="function")throw Error(E(280));var t=e.stateNode;t&&(t=Ii(t),Kl(e.stateNode,e.type,t))}}function Uu(e){fn?pn?pn.push(e):pn=[e]:fn=e}function Bu(){if(fn){var e=fn,t=pn;if(pn=fn=null,$s(e),t)for(e=0;e<t.length;e++)$s(t[e])}}function $u(e,t){return e(t)}function Hu(){}var ol=!1;function Vu(e,t,n){if(ol)return e(t,n);ol=!0;try{return $u(e,t,n)}finally{ol=!1,(fn!==null||pn!==null)&&(Hu(),Bu())}}function tr(e,t){var n=e.stateNode;if(n===null)return null;var r=Ii(n);if(r===null)return null;n=r[t];e:switch(t){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(r=!r.disabled)||(e=e.type,r=!(e==="button"||e==="input"||e==="select"||e==="textarea")),e=!r;break e;default:e=!1}if(e)return null;if(n&&typeof n!="function")throw Error(E(231,t,typeof n));return n}var Ql=!1;if(lt)try{var zn={};Object.defineProperty(zn,"passive",{get:function(){Ql=!0}}),window.addEventListener("test",zn,zn),window.removeEventListener("test",zn,zn)}catch{Ql=!1}function Af(e,t,n,r,i,l,o,s,a){var c=Array.prototype.slice.call(arguments,3);try{t.apply(n,c)}catch(f){this.onError(f)}}var Wn=!1,ui=null,ci=!1,Gl=null,Mf={onError:function(e){Wn=!0,ui=e}};function Ff(e,t,n,r,i,l,o,s,a){Wn=!1,ui=null,Af.apply(Mf,arguments)}function If(e,t,n,r,i,l,o,s,a){if(Ff.apply(this,arguments),Wn){if(Wn){var c=ui;Wn=!1,ui=null}else throw Error(E(198));ci||(ci=!0,Gl=c)}}function Gt(e){var t=e,n=e;if(e.alternate)for(;t.return;)t=t.return;else{e=t;do t=e,t.flags&4098&&(n=t.return),e=t.return;while(e)}return t.tag===3?n:null}function Wu(e){if(e.tag===13){var t=e.memoizedState;if(t===null&&(e=e.alternate,e!==null&&(t=e.memoizedState)),t!==null)return t.dehydrated}return null}function Hs(e){if(Gt(e)!==e)throw Error(E(188))}function Df(e){var t=e.alternate;if(!t){if(t=Gt(e),t===null)throw Error(E(188));return t!==e?null:e}for(var n=e,r=t;;){var i=n.return;if(i===null)break;var l=i.alternate;if(l===null){if(r=i.return,r!==null){n=r;continue}break}if(i.child===l.child){for(l=i.child;l;){if(l===n)return Hs(i),e;if(l===r)return Hs(i),t;l=l.sibling}throw Error(E(188))}if(n.return!==r.return)n=i,r=l;else{for(var o=!1,s=i.child;s;){if(s===n){o=!0,n=i,r=l;break}if(s===r){o=!0,r=i,n=l;break}s=s.sibling}if(!o){for(s=l.child;s;){if(s===n){o=!0,n=l,r=i;break}if(s===r){o=!0,r=l,n=i;break}s=s.sibling}if(!o)throw Error(E(189))}}if(n.alternate!==r)throw Error(E(190))}if(n.tag!==3)throw Error(E(188));return n.stateNode.current===n?e:t}function Ku(e){return e=Df(e),e!==null?Qu(e):null}function Qu(e){if(e.tag===5||e.tag===6)return e;for(e=e.child;e!==null;){var t=Qu(e);if(t!==null)return t;e=e.sibling}return null}var Gu=_e.unstable_scheduleCallback,Vs=_e.unstable_cancelCallback,Uf=_e.unstable_shouldYield,Bf=_e.unstable_requestPaint,G=_e.unstable_now,$f=_e.unstable_getCurrentPriorityLevel,Ho=_e.unstable_ImmediatePriority,qu=_e.unstable_UserBlockingPriority,di=_e.unstable_NormalPriority,Hf=_e.unstable_LowPriority,Yu=_e.unstable_IdlePriority,Li=null,Je=null;function Vf(e){if(Je&&typeof Je.onCommitFiberRoot=="function")try{Je.onCommitFiberRoot(Li,e,void 0,(e.current.flags&128)===128)}catch{}}var $e=Math.clz32?Math.clz32:Qf,Wf=Math.log,Kf=Math.LN2;function Qf(e){return e>>>=0,e===0?32:31-(Wf(e)/Kf|0)|0}var Or=64,Lr=4194304;function $n(e){switch(e&-e){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return e&4194240;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return e&130023424;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 1073741824;default:return e}}function fi(e,t){var n=e.pendingLanes;if(n===0)return 0;var r=0,i=e.suspendedLanes,l=e.pingedLanes,o=n&268435455;if(o!==0){var s=o&~i;s!==0?r=$n(s):(l&=o,l!==0&&(r=$n(l)))}else o=n&~i,o!==0?r=$n(o):l!==0&&(r=$n(l));if(r===0)return 0;if(t!==0&&t!==r&&!(t&i)&&(i=r&-r,l=t&-t,i>=l||i===16&&(l&4194240)!==0))return t;if(r&4&&(r|=n&16),t=e.entangledLanes,t!==0)for(e=e.entanglements,t&=r;0<t;)n=31-$e(t),i=1<<n,r|=e[n],t&=~i;return r}function Gf(e,t){switch(e){case 1:case 2:case 4:return t+250;case 8:case 16:case 32:case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return t+5e3;case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:return-1;case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function qf(e,t){for(var n=e.suspendedLanes,r=e.pingedLanes,i=e.expirationTimes,l=e.pendingLanes;0<l;){var o=31-$e(l),s=1<<o,a=i[o];a===-1?(!(s&n)||s&r)&&(i[o]=Gf(s,t)):a<=t&&(e.expiredLanes|=s),l&=~s}}function ql(e){return e=e.pendingLanes&-1073741825,e!==0?e:e&1073741824?1073741824:0}function Xu(){var e=Or;return Or<<=1,!(Or&4194240)&&(Or=64),e}function sl(e){for(var t=[],n=0;31>n;n++)t.push(e);return t}function vr(e,t,n){e.pendingLanes|=t,t!==536870912&&(e.suspendedLanes=0,e.pingedLanes=0),e=e.eventTimes,t=31-$e(t),e[t]=n}function Yf(e,t){var n=e.pendingLanes&~t;e.pendingLanes=t,e.suspendedLanes=0,e.pingedLanes=0,e.expiredLanes&=t,e.mutableReadLanes&=t,e.entangledLanes&=t,t=e.entanglements;var r=e.eventTimes;for(e=e.expirationTimes;0<n;){var i=31-$e(n),l=1<<i;t[i]=0,r[i]=-1,e[i]=-1,n&=~l}}function Vo(e,t){var n=e.entangledLanes|=t;for(e=e.entanglements;n;){var r=31-$e(n),i=1<<r;i&t|e[r]&t&&(e[r]|=t),n&=~i}}var F=0;function Ju(e){return e&=-e,1<e?4<e?e&268435455?16:536870912:4:1}var Zu,Wo,ec,tc,nc,Yl=!1,Ar=[],vt=null,xt=null,wt=null,nr=new Map,rr=new Map,mt=[],Xf="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");function Ws(e,t){switch(e){case"focusin":case"focusout":vt=null;break;case"dragenter":case"dragleave":xt=null;break;case"mouseover":case"mouseout":wt=null;break;case"pointerover":case"pointerout":nr.delete(t.pointerId);break;case"gotpointercapture":case"lostpointercapture":rr.delete(t.pointerId)}}function On(e,t,n,r,i,l){return e===null||e.nativeEvent!==l?(e={blockedOn:t,domEventName:n,eventSystemFlags:r,nativeEvent:l,targetContainers:[i]},t!==null&&(t=wr(t),t!==null&&Wo(t)),e):(e.eventSystemFlags|=r,t=e.targetContainers,i!==null&&t.indexOf(i)===-1&&t.push(i),e)}function Jf(e,t,n,r,i){switch(t){case"focusin":return vt=On(vt,e,t,n,r,i),!0;case"dragenter":return xt=On(xt,e,t,n,r,i),!0;case"mouseover":return wt=On(wt,e,t,n,r,i),!0;case"pointerover":var l=i.pointerId;return nr.set(l,On(nr.get(l)||null,e,t,n,r,i)),!0;case"gotpointercapture":return l=i.pointerId,rr.set(l,On(rr.get(l)||null,e,t,n,r,i)),!0}return!1}function rc(e){var t=Lt(e.target);if(t!==null){var n=Gt(t);if(n!==null){if(t=n.tag,t===13){if(t=Wu(n),t!==null){e.blockedOn=t,nc(e.priority,function(){ec(n)});return}}else if(t===3&&n.stateNode.current.memoizedState.isDehydrated){e.blockedOn=n.tag===3?n.stateNode.containerInfo:null;return}}}e.blockedOn=null}function qr(e){if(e.blockedOn!==null)return!1;for(var t=e.targetContainers;0<t.length;){var n=Xl(e.domEventName,e.eventSystemFlags,t[0],e.nativeEvent);if(n===null){n=e.nativeEvent;var r=new n.constructor(n.type,n);Wl=r,n.target.dispatchEvent(r),Wl=null}else return t=wr(n),t!==null&&Wo(t),e.blockedOn=n,!1;t.shift()}return!0}function Ks(e,t,n){qr(e)&&n.delete(t)}function Zf(){Yl=!1,vt!==null&&qr(vt)&&(vt=null),xt!==null&&qr(xt)&&(xt=null),wt!==null&&qr(wt)&&(wt=null),nr.forEach(Ks),rr.forEach(Ks)}function Ln(e,t){e.blockedOn===t&&(e.blockedOn=null,Yl||(Yl=!0,_e.unstable_scheduleCallback(_e.unstable_NormalPriority,Zf)))}function ir(e){function t(i){return Ln(i,e)}if(0<Ar.length){Ln(Ar[0],e);for(var n=1;n<Ar.length;n++){var r=Ar[n];r.blockedOn===e&&(r.blockedOn=null)}}for(vt!==null&&Ln(vt,e),xt!==null&&Ln(xt,e),wt!==null&&Ln(wt,e),nr.forEach(t),rr.forEach(t),n=0;n<mt.length;n++)r=mt[n],r.blockedOn===e&&(r.blockedOn=null);for(;0<mt.length&&(n=mt[0],n.blockedOn===null);)rc(n),n.blockedOn===null&&mt.shift()}var mn=ut.ReactCurrentBatchConfig,pi=!0;function ep(e,t,n,r){var i=F,l=mn.transition;mn.transition=null;try{F=1,Ko(e,t,n,r)}finally{F=i,mn.transition=l}}function tp(e,t,n,r){var i=F,l=mn.transition;mn.transition=null;try{F=4,Ko(e,t,n,r)}finally{F=i,mn.transition=l}}function Ko(e,t,n,r){if(pi){var i=Xl(e,t,n,r);if(i===null)yl(e,t,r,mi,n),Ws(e,r);else if(Jf(i,e,t,n,r))r.stopPropagation();else if(Ws(e,r),t&4&&-1<Xf.indexOf(e)){for(;i!==null;){var l=wr(i);if(l!==null&&Zu(l),l=Xl(e,t,n,r),l===null&&yl(e,t,r,mi,n),l===i)break;i=l}i!==null&&r.stopPropagation()}else yl(e,t,r,null,n)}}var mi=null;function Xl(e,t,n,r){if(mi=null,e=$o(r),e=Lt(e),e!==null)if(t=Gt(e),t===null)e=null;else if(n=t.tag,n===13){if(e=Wu(t),e!==null)return e;e=null}else if(n===3){if(t.stateNode.current.memoizedState.isDehydrated)return t.tag===3?t.stateNode.containerInfo:null;e=null}else t!==e&&(e=null);return mi=e,null}function ic(e){switch(e){case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 1;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"toggle":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 4;case"message":switch($f()){case Ho:return 1;case qu:return 4;case di:case Hf:return 16;case Yu:return 536870912;default:return 16}default:return 16}}var gt=null,Qo=null,Yr=null;function lc(){if(Yr)return Yr;var e,t=Qo,n=t.length,r,i="value"in gt?gt.value:gt.textContent,l=i.length;for(e=0;e<n&&t[e]===i[e];e++);var o=n-e;for(r=1;r<=o&&t[n-r]===i[l-r];r++);return Yr=i.slice(e,1<r?1-r:void 0)}function Xr(e){var t=e.keyCode;return"charCode"in e?(e=e.charCode,e===0&&t===13&&(e=13)):e=t,e===10&&(e=13),32<=e||e===13?e:0}function Mr(){return!0}function Qs(){return!1}function Te(e){function t(n,r,i,l,o){this._reactName=n,this._targetInst=i,this.type=r,this.nativeEvent=l,this.target=o,this.currentTarget=null;for(var s in e)e.hasOwnProperty(s)&&(n=e[s],this[s]=n?n(l):l[s]);return this.isDefaultPrevented=(l.defaultPrevented!=null?l.defaultPrevented:l.returnValue===!1)?Mr:Qs,this.isPropagationStopped=Qs,this}return K(t.prototype,{preventDefault:function(){this.defaultPrevented=!0;var n=this.nativeEvent;n&&(n.preventDefault?n.preventDefault():typeof n.returnValue!="unknown"&&(n.returnValue=!1),this.isDefaultPrevented=Mr)},stopPropagation:function(){var n=this.nativeEvent;n&&(n.stopPropagation?n.stopPropagation():typeof n.cancelBubble!="unknown"&&(n.cancelBubble=!0),this.isPropagationStopped=Mr)},persist:function(){},isPersistent:Mr}),t}var Rn={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(e){return e.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},Go=Te(Rn),xr=K({},Rn,{view:0,detail:0}),np=Te(xr),al,ul,An,Ai=K({},xr,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:qo,button:0,buttons:0,relatedTarget:function(e){return e.relatedTarget===void 0?e.fromElement===e.srcElement?e.toElement:e.fromElement:e.relatedTarget},movementX:function(e){return"movementX"in e?e.movementX:(e!==An&&(An&&e.type==="mousemove"?(al=e.screenX-An.screenX,ul=e.screenY-An.screenY):ul=al=0,An=e),al)},movementY:function(e){return"movementY"in e?e.movementY:ul}}),Gs=Te(Ai),rp=K({},Ai,{dataTransfer:0}),ip=Te(rp),lp=K({},xr,{relatedTarget:0}),cl=Te(lp),op=K({},Rn,{animationName:0,elapsedTime:0,pseudoElement:0}),sp=Te(op),ap=K({},Rn,{clipboardData:function(e){return"clipboardData"in e?e.clipboardData:window.clipboardData}}),up=Te(ap),cp=K({},Rn,{data:0}),qs=Te(cp),dp={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},fp={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},pp={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function mp(e){var t=this.nativeEvent;return t.getModifierState?t.getModifierState(e):(e=pp[e])?!!t[e]:!1}function qo(){return mp}var hp=K({},xr,{key:function(e){if(e.key){var t=dp[e.key]||e.key;if(t!=="Unidentified")return t}return e.type==="keypress"?(e=Xr(e),e===13?"Enter":String.fromCharCode(e)):e.type==="keydown"||e.type==="keyup"?fp[e.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:qo,charCode:function(e){return e.type==="keypress"?Xr(e):0},keyCode:function(e){return e.type==="keydown"||e.type==="keyup"?e.keyCode:0},which:function(e){return e.type==="keypress"?Xr(e):e.type==="keydown"||e.type==="keyup"?e.keyCode:0}}),gp=Te(hp),yp=K({},Ai,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),Ys=Te(yp),vp=K({},xr,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:qo}),xp=Te(vp),wp=K({},Rn,{propertyName:0,elapsedTime:0,pseudoElement:0}),Sp=Te(wp),kp=K({},Ai,{deltaX:function(e){return"deltaX"in e?e.deltaX:"wheelDeltaX"in e?-e.wheelDeltaX:0},deltaY:function(e){return"deltaY"in e?e.deltaY:"wheelDeltaY"in e?-e.wheelDeltaY:"wheelDelta"in e?-e.wheelDelta:0},deltaZ:0,deltaMode:0}),Ep=Te(kp),Np=[9,13,27,32],Yo=lt&&"CompositionEvent"in window,Kn=null;lt&&"documentMode"in document&&(Kn=document.documentMode);var jp=lt&&"TextEvent"in window&&!Kn,oc=lt&&(!Yo||Kn&&8<Kn&&11>=Kn),Xs=" ",Js=!1;function sc(e,t){switch(e){case"keyup":return Np.indexOf(t.keyCode)!==-1;case"keydown":return t.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function ac(e){return e=e.detail,typeof e=="object"&&"data"in e?e.data:null}var en=!1;function Cp(e,t){switch(e){case"compositionend":return ac(t);case"keypress":return t.which!==32?null:(Js=!0,Xs);case"textInput":return e=t.data,e===Xs&&Js?null:e;default:return null}}function _p(e,t){if(en)return e==="compositionend"||!Yo&&sc(e,t)?(e=lc(),Yr=Qo=gt=null,en=!1,e):null;switch(e){case"paste":return null;case"keypress":if(!(t.ctrlKey||t.altKey||t.metaKey)||t.ctrlKey&&t.altKey){if(t.char&&1<t.char.length)return t.char;if(t.which)return String.fromCharCode(t.which)}return null;case"compositionend":return oc&&t.locale!=="ko"?null:t.data;default:return null}}var Rp={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function Zs(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t==="input"?!!Rp[e.type]:t==="textarea"}function uc(e,t,n,r){Uu(r),t=hi(t,"onChange"),0<t.length&&(n=new Go("onChange","change",null,n,r),e.push({event:n,listeners:t}))}var Qn=null,lr=null;function Tp(e){wc(e,0)}function Mi(e){var t=rn(e);if(Ou(t))return e}function bp(e,t){if(e==="change")return t}var cc=!1;if(lt){var dl;if(lt){var fl="oninput"in document;if(!fl){var ea=document.createElement("div");ea.setAttribute("oninput","return;"),fl=typeof ea.oninput=="function"}dl=fl}else dl=!1;cc=dl&&(!document.documentMode||9<document.documentMode)}function ta(){Qn&&(Qn.detachEvent("onpropertychange",dc),lr=Qn=null)}function dc(e){if(e.propertyName==="value"&&Mi(lr)){var t=[];uc(t,lr,e,$o(e)),Vu(Tp,t)}}function Pp(e,t,n){e==="focusin"?(ta(),Qn=t,lr=n,Qn.attachEvent("onpropertychange",dc)):e==="focusout"&&ta()}function zp(e){if(e==="selectionchange"||e==="keyup"||e==="keydown")return Mi(lr)}function Op(e,t){if(e==="click")return Mi(t)}function Lp(e,t){if(e==="input"||e==="change")return Mi(t)}function Ap(e,t){return e===t&&(e!==0||1/e===1/t)||e!==e&&t!==t}var Ve=typeof Object.is=="function"?Object.is:Ap;function or(e,t){if(Ve(e,t))return!0;if(typeof e!="object"||e===null||typeof t!="object"||t===null)return!1;var n=Object.keys(e),r=Object.keys(t);if(n.length!==r.length)return!1;for(r=0;r<n.length;r++){var i=n[r];if(!Ol.call(t,i)||!Ve(e[i],t[i]))return!1}return!0}function na(e){for(;e&&e.firstChild;)e=e.firstChild;return e}function ra(e,t){var n=na(e);e=0;for(var r;n;){if(n.nodeType===3){if(r=e+n.textContent.length,e<=t&&r>=t)return{node:n,offset:t-e};e=r}e:{for(;n;){if(n.nextSibling){n=n.nextSibling;break e}n=n.parentNode}n=void 0}n=na(n)}}function fc(e,t){return e&&t?e===t?!0:e&&e.nodeType===3?!1:t&&t.nodeType===3?fc(e,t.parentNode):"contains"in e?e.contains(t):e.compareDocumentPosition?!!(e.compareDocumentPosition(t)&16):!1:!1}function pc(){for(var e=window,t=ai();t instanceof e.HTMLIFrameElement;){try{var n=typeof t.contentWindow.location.href=="string"}catch{n=!1}if(n)e=t.contentWindow;else break;t=ai(e.document)}return t}function Xo(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t&&(t==="input"&&(e.type==="text"||e.type==="search"||e.type==="tel"||e.type==="url"||e.type==="password")||t==="textarea"||e.contentEditable==="true")}function Mp(e){var t=pc(),n=e.focusedElem,r=e.selectionRange;if(t!==n&&n&&n.ownerDocument&&fc(n.ownerDocument.documentElement,n)){if(r!==null&&Xo(n)){if(t=r.start,e=r.end,e===void 0&&(e=t),"selectionStart"in n)n.selectionStart=t,n.selectionEnd=Math.min(e,n.value.length);else if(e=(t=n.ownerDocument||document)&&t.defaultView||window,e.getSelection){e=e.getSelection();var i=n.textContent.length,l=Math.min(r.start,i);r=r.end===void 0?l:Math.min(r.end,i),!e.extend&&l>r&&(i=r,r=l,l=i),i=ra(n,l);var o=ra(n,r);i&&o&&(e.rangeCount!==1||e.anchorNode!==i.node||e.anchorOffset!==i.offset||e.focusNode!==o.node||e.focusOffset!==o.offset)&&(t=t.createRange(),t.setStart(i.node,i.offset),e.removeAllRanges(),l>r?(e.addRange(t),e.extend(o.node,o.offset)):(t.setEnd(o.node,o.offset),e.addRange(t)))}}for(t=[],e=n;e=e.parentNode;)e.nodeType===1&&t.push({element:e,left:e.scrollLeft,top:e.scrollTop});for(typeof n.focus=="function"&&n.focus(),n=0;n<t.length;n++)e=t[n],e.element.scrollLeft=e.left,e.element.scrollTop=e.top}}var Fp=lt&&"documentMode"in document&&11>=document.documentMode,tn=null,Jl=null,Gn=null,Zl=!1;function ia(e,t,n){var r=n.window===n?n.document:n.nodeType===9?n:n.ownerDocument;Zl||tn==null||tn!==ai(r)||(r=tn,"selectionStart"in r&&Xo(r)?r={start:r.selectionStart,end:r.selectionEnd}:(r=(r.ownerDocument&&r.ownerDocument.defaultView||window).getSelection(),r={anchorNode:r.anchorNode,anchorOffset:r.anchorOffset,focusNode:r.focusNode,focusOffset:r.focusOffset}),Gn&&or(Gn,r)||(Gn=r,r=hi(Jl,"onSelect"),0<r.length&&(t=new Go("onSelect","select",null,t,n),e.push({event:t,listeners:r}),t.target=tn)))}function Fr(e,t){var n={};return n[e.toLowerCase()]=t.toLowerCase(),n["Webkit"+e]="webkit"+t,n["Moz"+e]="moz"+t,n}var nn={animationend:Fr("Animation","AnimationEnd"),animationiteration:Fr("Animation","AnimationIteration"),animationstart:Fr("Animation","AnimationStart"),transitionend:Fr("Transition","TransitionEnd")},pl={},mc={};lt&&(mc=document.createElement("div").style,"AnimationEvent"in window||(delete nn.animationend.animation,delete nn.animationiteration.animation,delete nn.animationstart.animation),"TransitionEvent"in window||delete nn.transitionend.transition);function Fi(e){if(pl[e])return pl[e];if(!nn[e])return e;var t=nn[e],n;for(n in t)if(t.hasOwnProperty(n)&&n in mc)return pl[e]=t[n];return e}var hc=Fi("animationend"),gc=Fi("animationiteration"),yc=Fi("animationstart"),vc=Fi("transitionend"),xc=new Map,la="abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");function Rt(e,t){xc.set(e,t),Qt(t,[e])}for(var ml=0;ml<la.length;ml++){var hl=la[ml],Ip=hl.toLowerCase(),Dp=hl[0].toUpperCase()+hl.slice(1);Rt(Ip,"on"+Dp)}Rt(hc,"onAnimationEnd");Rt(gc,"onAnimationIteration");Rt(yc,"onAnimationStart");Rt("dblclick","onDoubleClick");Rt("focusin","onFocus");Rt("focusout","onBlur");Rt(vc,"onTransitionEnd");yn("onMouseEnter",["mouseout","mouseover"]);yn("onMouseLeave",["mouseout","mouseover"]);yn("onPointerEnter",["pointerout","pointerover"]);yn("onPointerLeave",["pointerout","pointerover"]);Qt("onChange","change click focusin focusout input keydown keyup selectionchange".split(" "));Qt("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));Qt("onBeforeInput",["compositionend","keypress","textInput","paste"]);Qt("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" "));Qt("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" "));Qt("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var Hn="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),Up=new Set("cancel close invalid load scroll toggle".split(" ").concat(Hn));function oa(e,t,n){var r=e.type||"unknown-event";e.currentTarget=n,If(r,t,void 0,e),e.currentTarget=null}function wc(e,t){t=(t&4)!==0;for(var n=0;n<e.length;n++){var r=e[n],i=r.event;r=r.listeners;e:{var l=void 0;if(t)for(var o=r.length-1;0<=o;o--){var s=r[o],a=s.instance,c=s.currentTarget;if(s=s.listener,a!==l&&i.isPropagationStopped())break e;oa(i,s,c),l=a}else for(o=0;o<r.length;o++){if(s=r[o],a=s.instance,c=s.currentTarget,s=s.listener,a!==l&&i.isPropagationStopped())break e;oa(i,s,c),l=a}}}if(ci)throw e=Gl,ci=!1,Gl=null,e}function B(e,t){var n=t[io];n===void 0&&(n=t[io]=new Set);var r=e+"__bubble";n.has(r)||(Sc(t,e,2,!1),n.add(r))}function gl(e,t,n){var r=0;t&&(r|=4),Sc(n,e,r,t)}var Ir="_reactListening"+Math.random().toString(36).slice(2);function sr(e){if(!e[Ir]){e[Ir]=!0,Ru.forEach(function(n){n!=="selectionchange"&&(Up.has(n)||gl(n,!1,e),gl(n,!0,e))});var t=e.nodeType===9?e:e.ownerDocument;t===null||t[Ir]||(t[Ir]=!0,gl("selectionchange",!1,t))}}function Sc(e,t,n,r){switch(ic(t)){case 1:var i=ep;break;case 4:i=tp;break;default:i=Ko}n=i.bind(null,t,n,e),i=void 0,!Ql||t!=="touchstart"&&t!=="touchmove"&&t!=="wheel"||(i=!0),r?i!==void 0?e.addEventListener(t,n,{capture:!0,passive:i}):e.addEventListener(t,n,!0):i!==void 0?e.addEventListener(t,n,{passive:i}):e.addEventListener(t,n,!1)}function yl(e,t,n,r,i){var l=r;if(!(t&1)&&!(t&2)&&r!==null)e:for(;;){if(r===null)return;var o=r.tag;if(o===3||o===4){var s=r.stateNode.containerInfo;if(s===i||s.nodeType===8&&s.parentNode===i)break;if(o===4)for(o=r.return;o!==null;){var a=o.tag;if((a===3||a===4)&&(a=o.stateNode.containerInfo,a===i||a.nodeType===8&&a.parentNode===i))return;o=o.return}for(;s!==null;){if(o=Lt(s),o===null)return;if(a=o.tag,a===5||a===6){r=l=o;continue e}s=s.parentNode}}r=r.return}Vu(function(){var c=l,f=$o(n),d=[];e:{var h=xc.get(e);if(h!==void 0){var w=Go,m=e;switch(e){case"keypress":if(Xr(n)===0)break e;case"keydown":case"keyup":w=gp;break;case"focusin":m="focus",w=cl;break;case"focusout":m="blur",w=cl;break;case"beforeblur":case"afterblur":w=cl;break;case"click":if(n.button===2)break e;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":w=Gs;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":w=ip;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":w=xp;break;case hc:case gc:case yc:w=sp;break;case vc:w=Sp;break;case"scroll":w=np;break;case"wheel":w=Ep;break;case"copy":case"cut":case"paste":w=up;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":w=Ys}var v=(t&4)!==0,k=!v&&e==="scroll",g=v?h!==null?h+"Capture":null:h;v=[];for(var p=c,y;p!==null;){y=p;var S=y.stateNode;if(y.tag===5&&S!==null&&(y=S,g!==null&&(S=tr(p,g),S!=null&&v.push(ar(p,S,y)))),k)break;p=p.return}0<v.length&&(h=new w(h,m,null,n,f),d.push({event:h,listeners:v}))}}if(!(t&7)){e:{if(h=e==="mouseover"||e==="pointerover",w=e==="mouseout"||e==="pointerout",h&&n!==Wl&&(m=n.relatedTarget||n.fromElement)&&(Lt(m)||m[ot]))break e;if((w||h)&&(h=f.window===f?f:(h=f.ownerDocument)?h.defaultView||h.parentWindow:window,w?(m=n.relatedTarget||n.toElement,w=c,m=m?Lt(m):null,m!==null&&(k=Gt(m),m!==k||m.tag!==5&&m.tag!==6)&&(m=null)):(w=null,m=c),w!==m)){if(v=Gs,S="onMouseLeave",g="onMouseEnter",p="mouse",(e==="pointerout"||e==="pointerover")&&(v=Ys,S="onPointerLeave",g="onPointerEnter",p="pointer"),k=w==null?h:rn(w),y=m==null?h:rn(m),h=new v(S,p+"leave",w,n,f),h.target=k,h.relatedTarget=y,S=null,Lt(f)===c&&(v=new v(g,p+"enter",m,n,f),v.target=y,v.relatedTarget=k,S=v),k=S,w&&m)t:{for(v=w,g=m,p=0,y=v;y;y=Xt(y))p++;for(y=0,S=g;S;S=Xt(S))y++;for(;0<p-y;)v=Xt(v),p--;for(;0<y-p;)g=Xt(g),y--;for(;p--;){if(v===g||g!==null&&v===g.alternate)break t;v=Xt(v),g=Xt(g)}v=null}else v=null;w!==null&&sa(d,h,w,v,!1),m!==null&&k!==null&&sa(d,k,m,v,!0)}}e:{if(h=c?rn(c):window,w=h.nodeName&&h.nodeName.toLowerCase(),w==="select"||w==="input"&&h.type==="file")var N=bp;else if(Zs(h))if(cc)N=Lp;else{N=zp;var R=Pp}else(w=h.nodeName)&&w.toLowerCase()==="input"&&(h.type==="checkbox"||h.type==="radio")&&(N=Op);if(N&&(N=N(e,c))){uc(d,N,n,f);break e}R&&R(e,h,c),e==="focusout"&&(R=h._wrapperState)&&R.controlled&&h.type==="number"&&Ul(h,"number",h.value)}switch(R=c?rn(c):window,e){case"focusin":(Zs(R)||R.contentEditable==="true")&&(tn=R,Jl=c,Gn=null);break;case"focusout":Gn=Jl=tn=null;break;case"mousedown":Zl=!0;break;case"contextmenu":case"mouseup":case"dragend":Zl=!1,ia(d,n,f);break;case"selectionchange":if(Fp)break;case"keydown":case"keyup":ia(d,n,f)}var C;if(Yo)e:{switch(e){case"compositionstart":var T="onCompositionStart";break e;case"compositionend":T="onCompositionEnd";break e;case"compositionupdate":T="onCompositionUpdate";break e}T=void 0}else en?sc(e,n)&&(T="onCompositionEnd"):e==="keydown"&&n.keyCode===229&&(T="onCompositionStart");T&&(oc&&n.locale!=="ko"&&(en||T!=="onCompositionStart"?T==="onCompositionEnd"&&en&&(C=lc()):(gt=f,Qo="value"in gt?gt.value:gt.textContent,en=!0)),R=hi(c,T),0<R.length&&(T=new qs(T,e,null,n,f),d.push({event:T,listeners:R}),C?T.data=C:(C=ac(n),C!==null&&(T.data=C)))),(C=jp?Cp(e,n):_p(e,n))&&(c=hi(c,"onBeforeInput"),0<c.length&&(f=new qs("onBeforeInput","beforeinput",null,n,f),d.push({event:f,listeners:c}),f.data=C))}wc(d,t)})}function ar(e,t,n){return{instance:e,listener:t,currentTarget:n}}function hi(e,t){for(var n=t+"Capture",r=[];e!==null;){var i=e,l=i.stateNode;i.tag===5&&l!==null&&(i=l,l=tr(e,n),l!=null&&r.unshift(ar(e,l,i)),l=tr(e,t),l!=null&&r.push(ar(e,l,i))),e=e.return}return r}function Xt(e){if(e===null)return null;do e=e.return;while(e&&e.tag!==5);return e||null}function sa(e,t,n,r,i){for(var l=t._reactName,o=[];n!==null&&n!==r;){var s=n,a=s.alternate,c=s.stateNode;if(a!==null&&a===r)break;s.tag===5&&c!==null&&(s=c,i?(a=tr(n,l),a!=null&&o.unshift(ar(n,a,s))):i||(a=tr(n,l),a!=null&&o.push(ar(n,a,s)))),n=n.return}o.length!==0&&e.push({event:t,listeners:o})}var Bp=/\r\n?/g,$p=/\u0000|\uFFFD/g;function aa(e){return(typeof e=="string"?e:""+e).replace(Bp,`
`).replace($p,"")}function Dr(e,t,n){if(t=aa(t),aa(e)!==t&&n)throw Error(E(425))}function gi(){}var eo=null,to=null;function no(e,t){return e==="textarea"||e==="noscript"||typeof t.children=="string"||typeof t.children=="number"||typeof t.dangerouslySetInnerHTML=="object"&&t.dangerouslySetInnerHTML!==null&&t.dangerouslySetInnerHTML.__html!=null}var ro=typeof setTimeout=="function"?setTimeout:void 0,Hp=typeof clearTimeout=="function"?clearTimeout:void 0,ua=typeof Promise=="function"?Promise:void 0,Vp=typeof queueMicrotask=="function"?queueMicrotask:typeof ua<"u"?function(e){return ua.resolve(null).then(e).catch(Wp)}:ro;function Wp(e){setTimeout(function(){throw e})}function vl(e,t){var n=t,r=0;do{var i=n.nextSibling;if(e.removeChild(n),i&&i.nodeType===8)if(n=i.data,n==="/$"){if(r===0){e.removeChild(i),ir(t);return}r--}else n!=="$"&&n!=="$?"&&n!=="$!"||r++;n=i}while(n);ir(t)}function St(e){for(;e!=null;e=e.nextSibling){var t=e.nodeType;if(t===1||t===3)break;if(t===8){if(t=e.data,t==="$"||t==="$!"||t==="$?")break;if(t==="/$")return null}}return e}function ca(e){e=e.previousSibling;for(var t=0;e;){if(e.nodeType===8){var n=e.data;if(n==="$"||n==="$!"||n==="$?"){if(t===0)return e;t--}else n==="/$"&&t++}e=e.previousSibling}return null}var Tn=Math.random().toString(36).slice(2),Xe="__reactFiber$"+Tn,ur="__reactProps$"+Tn,ot="__reactContainer$"+Tn,io="__reactEvents$"+Tn,Kp="__reactListeners$"+Tn,Qp="__reactHandles$"+Tn;function Lt(e){var t=e[Xe];if(t)return t;for(var n=e.parentNode;n;){if(t=n[ot]||n[Xe]){if(n=t.alternate,t.child!==null||n!==null&&n.child!==null)for(e=ca(e);e!==null;){if(n=e[Xe])return n;e=ca(e)}return t}e=n,n=e.parentNode}return null}function wr(e){return e=e[Xe]||e[ot],!e||e.tag!==5&&e.tag!==6&&e.tag!==13&&e.tag!==3?null:e}function rn(e){if(e.tag===5||e.tag===6)return e.stateNode;throw Error(E(33))}function Ii(e){return e[ur]||null}var lo=[],ln=-1;function Tt(e){return{current:e}}function $(e){0>ln||(e.current=lo[ln],lo[ln]=null,ln--)}function D(e,t){ln++,lo[ln]=e.current,e.current=t}var _t={},ue=Tt(_t),ve=Tt(!1),Bt=_t;function vn(e,t){var n=e.type.contextTypes;if(!n)return _t;var r=e.stateNode;if(r&&r.__reactInternalMemoizedUnmaskedChildContext===t)return r.__reactInternalMemoizedMaskedChildContext;var i={},l;for(l in n)i[l]=t[l];return r&&(e=e.stateNode,e.__reactInternalMemoizedUnmaskedChildContext=t,e.__reactInternalMemoizedMaskedChildContext=i),i}function xe(e){return e=e.childContextTypes,e!=null}function yi(){$(ve),$(ue)}function da(e,t,n){if(ue.current!==_t)throw Error(E(168));D(ue,t),D(ve,n)}function kc(e,t,n){var r=e.stateNode;if(t=t.childContextTypes,typeof r.getChildContext!="function")return n;r=r.getChildContext();for(var i in r)if(!(i in t))throw Error(E(108,Pf(e)||"Unknown",i));return K({},n,r)}function vi(e){return e=(e=e.stateNode)&&e.__reactInternalMemoizedMergedChildContext||_t,Bt=ue.current,D(ue,e),D(ve,ve.current),!0}function fa(e,t,n){var r=e.stateNode;if(!r)throw Error(E(169));n?(e=kc(e,t,Bt),r.__reactInternalMemoizedMergedChildContext=e,$(ve),$(ue),D(ue,e)):$(ve),D(ve,n)}var tt=null,Di=!1,xl=!1;function Ec(e){tt===null?tt=[e]:tt.push(e)}function Gp(e){Di=!0,Ec(e)}function bt(){if(!xl&&tt!==null){xl=!0;var e=0,t=F;try{var n=tt;for(F=1;e<n.length;e++){var r=n[e];do r=r(!0);while(r!==null)}tt=null,Di=!1}catch(i){throw tt!==null&&(tt=tt.slice(e+1)),Gu(Ho,bt),i}finally{F=t,xl=!1}}return null}var on=[],sn=0,xi=null,wi=0,Pe=[],ze=0,$t=null,nt=1,rt="";function zt(e,t){on[sn++]=wi,on[sn++]=xi,xi=e,wi=t}function Nc(e,t,n){Pe[ze++]=nt,Pe[ze++]=rt,Pe[ze++]=$t,$t=e;var r=nt;e=rt;var i=32-$e(r)-1;r&=~(1<<i),n+=1;var l=32-$e(t)+i;if(30<l){var o=i-i%5;l=(r&(1<<o)-1).toString(32),r>>=o,i-=o,nt=1<<32-$e(t)+i|n<<i|r,rt=l+e}else nt=1<<l|n<<i|r,rt=e}function Jo(e){e.return!==null&&(zt(e,1),Nc(e,1,0))}function Zo(e){for(;e===xi;)xi=on[--sn],on[sn]=null,wi=on[--sn],on[sn]=null;for(;e===$t;)$t=Pe[--ze],Pe[ze]=null,rt=Pe[--ze],Pe[ze]=null,nt=Pe[--ze],Pe[ze]=null}var Ce=null,Ne=null,H=!1,Be=null;function jc(e,t){var n=Oe(5,null,null,0);n.elementType="DELETED",n.stateNode=t,n.return=e,t=e.deletions,t===null?(e.deletions=[n],e.flags|=16):t.push(n)}function pa(e,t){switch(e.tag){case 5:var n=e.type;return t=t.nodeType!==1||n.toLowerCase()!==t.nodeName.toLowerCase()?null:t,t!==null?(e.stateNode=t,Ce=e,Ne=St(t.firstChild),!0):!1;case 6:return t=e.pendingProps===""||t.nodeType!==3?null:t,t!==null?(e.stateNode=t,Ce=e,Ne=null,!0):!1;case 13:return t=t.nodeType!==8?null:t,t!==null?(n=$t!==null?{id:nt,overflow:rt}:null,e.memoizedState={dehydrated:t,treeContext:n,retryLane:1073741824},n=Oe(18,null,null,0),n.stateNode=t,n.return=e,e.child=n,Ce=e,Ne=null,!0):!1;default:return!1}}function oo(e){return(e.mode&1)!==0&&(e.flags&128)===0}function so(e){if(H){var t=Ne;if(t){var n=t;if(!pa(e,t)){if(oo(e))throw Error(E(418));t=St(n.nextSibling);var r=Ce;t&&pa(e,t)?jc(r,n):(e.flags=e.flags&-4097|2,H=!1,Ce=e)}}else{if(oo(e))throw Error(E(418));e.flags=e.flags&-4097|2,H=!1,Ce=e}}}function ma(e){for(e=e.return;e!==null&&e.tag!==5&&e.tag!==3&&e.tag!==13;)e=e.return;Ce=e}function Ur(e){if(e!==Ce)return!1;if(!H)return ma(e),H=!0,!1;var t;if((t=e.tag!==3)&&!(t=e.tag!==5)&&(t=e.type,t=t!=="head"&&t!=="body"&&!no(e.type,e.memoizedProps)),t&&(t=Ne)){if(oo(e))throw Cc(),Error(E(418));for(;t;)jc(e,t),t=St(t.nextSibling)}if(ma(e),e.tag===13){if(e=e.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(E(317));e:{for(e=e.nextSibling,t=0;e;){if(e.nodeType===8){var n=e.data;if(n==="/$"){if(t===0){Ne=St(e.nextSibling);break e}t--}else n!=="$"&&n!=="$!"&&n!=="$?"||t++}e=e.nextSibling}Ne=null}}else Ne=Ce?St(e.stateNode.nextSibling):null;return!0}function Cc(){for(var e=Ne;e;)e=St(e.nextSibling)}function xn(){Ne=Ce=null,H=!1}function es(e){Be===null?Be=[e]:Be.push(e)}var qp=ut.ReactCurrentBatchConfig;function Mn(e,t,n){if(e=n.ref,e!==null&&typeof e!="function"&&typeof e!="object"){if(n._owner){if(n=n._owner,n){if(n.tag!==1)throw Error(E(309));var r=n.stateNode}if(!r)throw Error(E(147,e));var i=r,l=""+e;return t!==null&&t.ref!==null&&typeof t.ref=="function"&&t.ref._stringRef===l?t.ref:(t=function(o){var s=i.refs;o===null?delete s[l]:s[l]=o},t._stringRef=l,t)}if(typeof e!="string")throw Error(E(284));if(!n._owner)throw Error(E(290,e))}return e}function Br(e,t){throw e=Object.prototype.toString.call(t),Error(E(31,e==="[object Object]"?"object with keys {"+Object.keys(t).join(", ")+"}":e))}function ha(e){var t=e._init;return t(e._payload)}function _c(e){function t(g,p){if(e){var y=g.deletions;y===null?(g.deletions=[p],g.flags|=16):y.push(p)}}function n(g,p){if(!e)return null;for(;p!==null;)t(g,p),p=p.sibling;return null}function r(g,p){for(g=new Map;p!==null;)p.key!==null?g.set(p.key,p):g.set(p.index,p),p=p.sibling;return g}function i(g,p){return g=jt(g,p),g.index=0,g.sibling=null,g}function l(g,p,y){return g.index=y,e?(y=g.alternate,y!==null?(y=y.index,y<p?(g.flags|=2,p):y):(g.flags|=2,p)):(g.flags|=1048576,p)}function o(g){return e&&g.alternate===null&&(g.flags|=2),g}function s(g,p,y,S){return p===null||p.tag!==6?(p=Cl(y,g.mode,S),p.return=g,p):(p=i(p,y),p.return=g,p)}function a(g,p,y,S){var N=y.type;return N===Zt?f(g,p,y.props.children,S,y.key):p!==null&&(p.elementType===N||typeof N=="object"&&N!==null&&N.$$typeof===ft&&ha(N)===p.type)?(S=i(p,y.props),S.ref=Mn(g,p,y),S.return=g,S):(S=ii(y.type,y.key,y.props,null,g.mode,S),S.ref=Mn(g,p,y),S.return=g,S)}function c(g,p,y,S){return p===null||p.tag!==4||p.stateNode.containerInfo!==y.containerInfo||p.stateNode.implementation!==y.implementation?(p=_l(y,g.mode,S),p.return=g,p):(p=i(p,y.children||[]),p.return=g,p)}function f(g,p,y,S,N){return p===null||p.tag!==7?(p=Dt(y,g.mode,S,N),p.return=g,p):(p=i(p,y),p.return=g,p)}function d(g,p,y){if(typeof p=="string"&&p!==""||typeof p=="number")return p=Cl(""+p,g.mode,y),p.return=g,p;if(typeof p=="object"&&p!==null){switch(p.$$typeof){case br:return y=ii(p.type,p.key,p.props,null,g.mode,y),y.ref=Mn(g,null,p),y.return=g,y;case Jt:return p=_l(p,g.mode,y),p.return=g,p;case ft:var S=p._init;return d(g,S(p._payload),y)}if(Bn(p)||Pn(p))return p=Dt(p,g.mode,y,null),p.return=g,p;Br(g,p)}return null}function h(g,p,y,S){var N=p!==null?p.key:null;if(typeof y=="string"&&y!==""||typeof y=="number")return N!==null?null:s(g,p,""+y,S);if(typeof y=="object"&&y!==null){switch(y.$$typeof){case br:return y.key===N?a(g,p,y,S):null;case Jt:return y.key===N?c(g,p,y,S):null;case ft:return N=y._init,h(g,p,N(y._payload),S)}if(Bn(y)||Pn(y))return N!==null?null:f(g,p,y,S,null);Br(g,y)}return null}function w(g,p,y,S,N){if(typeof S=="string"&&S!==""||typeof S=="number")return g=g.get(y)||null,s(p,g,""+S,N);if(typeof S=="object"&&S!==null){switch(S.$$typeof){case br:return g=g.get(S.key===null?y:S.key)||null,a(p,g,S,N);case Jt:return g=g.get(S.key===null?y:S.key)||null,c(p,g,S,N);case ft:var R=S._init;return w(g,p,y,R(S._payload),N)}if(Bn(S)||Pn(S))return g=g.get(y)||null,f(p,g,S,N,null);Br(p,S)}return null}function m(g,p,y,S){for(var N=null,R=null,C=p,T=p=0,I=null;C!==null&&T<y.length;T++){C.index>T?(I=C,C=null):I=C.sibling;var O=h(g,C,y[T],S);if(O===null){C===null&&(C=I);break}e&&C&&O.alternate===null&&t(g,C),p=l(O,p,T),R===null?N=O:R.sibling=O,R=O,C=I}if(T===y.length)return n(g,C),H&&zt(g,T),N;if(C===null){for(;T<y.length;T++)C=d(g,y[T],S),C!==null&&(p=l(C,p,T),R===null?N=C:R.sibling=C,R=C);return H&&zt(g,T),N}for(C=r(g,C);T<y.length;T++)I=w(C,g,T,y[T],S),I!==null&&(e&&I.alternate!==null&&C.delete(I.key===null?T:I.key),p=l(I,p,T),R===null?N=I:R.sibling=I,R=I);return e&&C.forEach(function(me){return t(g,me)}),H&&zt(g,T),N}function v(g,p,y,S){var N=Pn(y);if(typeof N!="function")throw Error(E(150));if(y=N.call(y),y==null)throw Error(E(151));for(var R=N=null,C=p,T=p=0,I=null,O=y.next();C!==null&&!O.done;T++,O=y.next()){C.index>T?(I=C,C=null):I=C.sibling;var me=h(g,C,O.value,S);if(me===null){C===null&&(C=I);break}e&&C&&me.alternate===null&&t(g,C),p=l(me,p,T),R===null?N=me:R.sibling=me,R=me,C=I}if(O.done)return n(g,C),H&&zt(g,T),N;if(C===null){for(;!O.done;T++,O=y.next())O=d(g,O.value,S),O!==null&&(p=l(O,p,T),R===null?N=O:R.sibling=O,R=O);return H&&zt(g,T),N}for(C=r(g,C);!O.done;T++,O=y.next())O=w(C,g,T,O.value,S),O!==null&&(e&&O.alternate!==null&&C.delete(O.key===null?T:O.key),p=l(O,p,T),R===null?N=O:R.sibling=O,R=O);return e&&C.forEach(function(Ke){return t(g,Ke)}),H&&zt(g,T),N}function k(g,p,y,S){if(typeof y=="object"&&y!==null&&y.type===Zt&&y.key===null&&(y=y.props.children),typeof y=="object"&&y!==null){switch(y.$$typeof){case br:e:{for(var N=y.key,R=p;R!==null;){if(R.key===N){if(N=y.type,N===Zt){if(R.tag===7){n(g,R.sibling),p=i(R,y.props.children),p.return=g,g=p;break e}}else if(R.elementType===N||typeof N=="object"&&N!==null&&N.$$typeof===ft&&ha(N)===R.type){n(g,R.sibling),p=i(R,y.props),p.ref=Mn(g,R,y),p.return=g,g=p;break e}n(g,R);break}else t(g,R);R=R.sibling}y.type===Zt?(p=Dt(y.props.children,g.mode,S,y.key),p.return=g,g=p):(S=ii(y.type,y.key,y.props,null,g.mode,S),S.ref=Mn(g,p,y),S.return=g,g=S)}return o(g);case Jt:e:{for(R=y.key;p!==null;){if(p.key===R)if(p.tag===4&&p.stateNode.containerInfo===y.containerInfo&&p.stateNode.implementation===y.implementation){n(g,p.sibling),p=i(p,y.children||[]),p.return=g,g=p;break e}else{n(g,p);break}else t(g,p);p=p.sibling}p=_l(y,g.mode,S),p.return=g,g=p}return o(g);case ft:return R=y._init,k(g,p,R(y._payload),S)}if(Bn(y))return m(g,p,y,S);if(Pn(y))return v(g,p,y,S);Br(g,y)}return typeof y=="string"&&y!==""||typeof y=="number"?(y=""+y,p!==null&&p.tag===6?(n(g,p.sibling),p=i(p,y),p.return=g,g=p):(n(g,p),p=Cl(y,g.mode,S),p.return=g,g=p),o(g)):n(g,p)}return k}var wn=_c(!0),Rc=_c(!1),Si=Tt(null),ki=null,an=null,ts=null;function ns(){ts=an=ki=null}function rs(e){var t=Si.current;$(Si),e._currentValue=t}function ao(e,t,n){for(;e!==null;){var r=e.alternate;if((e.childLanes&t)!==t?(e.childLanes|=t,r!==null&&(r.childLanes|=t)):r!==null&&(r.childLanes&t)!==t&&(r.childLanes|=t),e===n)break;e=e.return}}function hn(e,t){ki=e,ts=an=null,e=e.dependencies,e!==null&&e.firstContext!==null&&(e.lanes&t&&(ye=!0),e.firstContext=null)}function Ae(e){var t=e._currentValue;if(ts!==e)if(e={context:e,memoizedValue:t,next:null},an===null){if(ki===null)throw Error(E(308));an=e,ki.dependencies={lanes:0,firstContext:e}}else an=an.next=e;return t}var At=null;function is(e){At===null?At=[e]:At.push(e)}function Tc(e,t,n,r){var i=t.interleaved;return i===null?(n.next=n,is(t)):(n.next=i.next,i.next=n),t.interleaved=n,st(e,r)}function st(e,t){e.lanes|=t;var n=e.alternate;for(n!==null&&(n.lanes|=t),n=e,e=e.return;e!==null;)e.childLanes|=t,n=e.alternate,n!==null&&(n.childLanes|=t),n=e,e=e.return;return n.tag===3?n.stateNode:null}var pt=!1;function ls(e){e.updateQueue={baseState:e.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,interleaved:null,lanes:0},effects:null}}function bc(e,t){e=e.updateQueue,t.updateQueue===e&&(t.updateQueue={baseState:e.baseState,firstBaseUpdate:e.firstBaseUpdate,lastBaseUpdate:e.lastBaseUpdate,shared:e.shared,effects:e.effects})}function it(e,t){return{eventTime:e,lane:t,tag:0,payload:null,callback:null,next:null}}function kt(e,t,n){var r=e.updateQueue;if(r===null)return null;if(r=r.shared,A&2){var i=r.pending;return i===null?t.next=t:(t.next=i.next,i.next=t),r.pending=t,st(e,n)}return i=r.interleaved,i===null?(t.next=t,is(r)):(t.next=i.next,i.next=t),r.interleaved=t,st(e,n)}function Jr(e,t,n){if(t=t.updateQueue,t!==null&&(t=t.shared,(n&4194240)!==0)){var r=t.lanes;r&=e.pendingLanes,n|=r,t.lanes=n,Vo(e,n)}}function ga(e,t){var n=e.updateQueue,r=e.alternate;if(r!==null&&(r=r.updateQueue,n===r)){var i=null,l=null;if(n=n.firstBaseUpdate,n!==null){do{var o={eventTime:n.eventTime,lane:n.lane,tag:n.tag,payload:n.payload,callback:n.callback,next:null};l===null?i=l=o:l=l.next=o,n=n.next}while(n!==null);l===null?i=l=t:l=l.next=t}else i=l=t;n={baseState:r.baseState,firstBaseUpdate:i,lastBaseUpdate:l,shared:r.shared,effects:r.effects},e.updateQueue=n;return}e=n.lastBaseUpdate,e===null?n.firstBaseUpdate=t:e.next=t,n.lastBaseUpdate=t}function Ei(e,t,n,r){var i=e.updateQueue;pt=!1;var l=i.firstBaseUpdate,o=i.lastBaseUpdate,s=i.shared.pending;if(s!==null){i.shared.pending=null;var a=s,c=a.next;a.next=null,o===null?l=c:o.next=c,o=a;var f=e.alternate;f!==null&&(f=f.updateQueue,s=f.lastBaseUpdate,s!==o&&(s===null?f.firstBaseUpdate=c:s.next=c,f.lastBaseUpdate=a))}if(l!==null){var d=i.baseState;o=0,f=c=a=null,s=l;do{var h=s.lane,w=s.eventTime;if((r&h)===h){f!==null&&(f=f.next={eventTime:w,lane:0,tag:s.tag,payload:s.payload,callback:s.callback,next:null});e:{var m=e,v=s;switch(h=t,w=n,v.tag){case 1:if(m=v.payload,typeof m=="function"){d=m.call(w,d,h);break e}d=m;break e;case 3:m.flags=m.flags&-65537|128;case 0:if(m=v.payload,h=typeof m=="function"?m.call(w,d,h):m,h==null)break e;d=K({},d,h);break e;case 2:pt=!0}}s.callback!==null&&s.lane!==0&&(e.flags|=64,h=i.effects,h===null?i.effects=[s]:h.push(s))}else w={eventTime:w,lane:h,tag:s.tag,payload:s.payload,callback:s.callback,next:null},f===null?(c=f=w,a=d):f=f.next=w,o|=h;if(s=s.next,s===null){if(s=i.shared.pending,s===null)break;h=s,s=h.next,h.next=null,i.lastBaseUpdate=h,i.shared.pending=null}}while(!0);if(f===null&&(a=d),i.baseState=a,i.firstBaseUpdate=c,i.lastBaseUpdate=f,t=i.shared.interleaved,t!==null){i=t;do o|=i.lane,i=i.next;while(i!==t)}else l===null&&(i.shared.lanes=0);Vt|=o,e.lanes=o,e.memoizedState=d}}function ya(e,t,n){if(e=t.effects,t.effects=null,e!==null)for(t=0;t<e.length;t++){var r=e[t],i=r.callback;if(i!==null){if(r.callback=null,r=n,typeof i!="function")throw Error(E(191,i));i.call(r)}}}var Sr={},Ze=Tt(Sr),cr=Tt(Sr),dr=Tt(Sr);function Mt(e){if(e===Sr)throw Error(E(174));return e}function os(e,t){switch(D(dr,t),D(cr,e),D(Ze,Sr),e=t.nodeType,e){case 9:case 11:t=(t=t.documentElement)?t.namespaceURI:$l(null,"");break;default:e=e===8?t.parentNode:t,t=e.namespaceURI||null,e=e.tagName,t=$l(t,e)}$(Ze),D(Ze,t)}function Sn(){$(Ze),$(cr),$(dr)}function Pc(e){Mt(dr.current);var t=Mt(Ze.current),n=$l(t,e.type);t!==n&&(D(cr,e),D(Ze,n))}function ss(e){cr.current===e&&($(Ze),$(cr))}var V=Tt(0);function Ni(e){for(var t=e;t!==null;){if(t.tag===13){var n=t.memoizedState;if(n!==null&&(n=n.dehydrated,n===null||n.data==="$?"||n.data==="$!"))return t}else if(t.tag===19&&t.memoizedProps.revealOrder!==void 0){if(t.flags&128)return t}else if(t.child!==null){t.child.return=t,t=t.child;continue}if(t===e)break;for(;t.sibling===null;){if(t.return===null||t.return===e)return null;t=t.return}t.sibling.return=t.return,t=t.sibling}return null}var wl=[];function as(){for(var e=0;e<wl.length;e++)wl[e]._workInProgressVersionPrimary=null;wl.length=0}var Zr=ut.ReactCurrentDispatcher,Sl=ut.ReactCurrentBatchConfig,Ht=0,W=null,X=null,Z=null,ji=!1,qn=!1,fr=0,Yp=0;function ie(){throw Error(E(321))}function us(e,t){if(t===null)return!1;for(var n=0;n<t.length&&n<e.length;n++)if(!Ve(e[n],t[n]))return!1;return!0}function cs(e,t,n,r,i,l){if(Ht=l,W=t,t.memoizedState=null,t.updateQueue=null,t.lanes=0,Zr.current=e===null||e.memoizedState===null?em:tm,e=n(r,i),qn){l=0;do{if(qn=!1,fr=0,25<=l)throw Error(E(301));l+=1,Z=X=null,t.updateQueue=null,Zr.current=nm,e=n(r,i)}while(qn)}if(Zr.current=Ci,t=X!==null&&X.next!==null,Ht=0,Z=X=W=null,ji=!1,t)throw Error(E(300));return e}function ds(){var e=fr!==0;return fr=0,e}function Ye(){var e={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return Z===null?W.memoizedState=Z=e:Z=Z.next=e,Z}function Me(){if(X===null){var e=W.alternate;e=e!==null?e.memoizedState:null}else e=X.next;var t=Z===null?W.memoizedState:Z.next;if(t!==null)Z=t,X=e;else{if(e===null)throw Error(E(310));X=e,e={memoizedState:X.memoizedState,baseState:X.baseState,baseQueue:X.baseQueue,queue:X.queue,next:null},Z===null?W.memoizedState=Z=e:Z=Z.next=e}return Z}function pr(e,t){return typeof t=="function"?t(e):t}function kl(e){var t=Me(),n=t.queue;if(n===null)throw Error(E(311));n.lastRenderedReducer=e;var r=X,i=r.baseQueue,l=n.pending;if(l!==null){if(i!==null){var o=i.next;i.next=l.next,l.next=o}r.baseQueue=i=l,n.pending=null}if(i!==null){l=i.next,r=r.baseState;var s=o=null,a=null,c=l;do{var f=c.lane;if((Ht&f)===f)a!==null&&(a=a.next={lane:0,action:c.action,hasEagerState:c.hasEagerState,eagerState:c.eagerState,next:null}),r=c.hasEagerState?c.eagerState:e(r,c.action);else{var d={lane:f,action:c.action,hasEagerState:c.hasEagerState,eagerState:c.eagerState,next:null};a===null?(s=a=d,o=r):a=a.next=d,W.lanes|=f,Vt|=f}c=c.next}while(c!==null&&c!==l);a===null?o=r:a.next=s,Ve(r,t.memoizedState)||(ye=!0),t.memoizedState=r,t.baseState=o,t.baseQueue=a,n.lastRenderedState=r}if(e=n.interleaved,e!==null){i=e;do l=i.lane,W.lanes|=l,Vt|=l,i=i.next;while(i!==e)}else i===null&&(n.lanes=0);return[t.memoizedState,n.dispatch]}function El(e){var t=Me(),n=t.queue;if(n===null)throw Error(E(311));n.lastRenderedReducer=e;var r=n.dispatch,i=n.pending,l=t.memoizedState;if(i!==null){n.pending=null;var o=i=i.next;do l=e(l,o.action),o=o.next;while(o!==i);Ve(l,t.memoizedState)||(ye=!0),t.memoizedState=l,t.baseQueue===null&&(t.baseState=l),n.lastRenderedState=l}return[l,r]}function zc(){}function Oc(e,t){var n=W,r=Me(),i=t(),l=!Ve(r.memoizedState,i);if(l&&(r.memoizedState=i,ye=!0),r=r.queue,fs(Mc.bind(null,n,r,e),[e]),r.getSnapshot!==t||l||Z!==null&&Z.memoizedState.tag&1){if(n.flags|=2048,mr(9,Ac.bind(null,n,r,i,t),void 0,null),ee===null)throw Error(E(349));Ht&30||Lc(n,t,i)}return i}function Lc(e,t,n){e.flags|=16384,e={getSnapshot:t,value:n},t=W.updateQueue,t===null?(t={lastEffect:null,stores:null},W.updateQueue=t,t.stores=[e]):(n=t.stores,n===null?t.stores=[e]:n.push(e))}function Ac(e,t,n,r){t.value=n,t.getSnapshot=r,Fc(t)&&Ic(e)}function Mc(e,t,n){return n(function(){Fc(t)&&Ic(e)})}function Fc(e){var t=e.getSnapshot;e=e.value;try{var n=t();return!Ve(e,n)}catch{return!0}}function Ic(e){var t=st(e,1);t!==null&&He(t,e,1,-1)}function va(e){var t=Ye();return typeof e=="function"&&(e=e()),t.memoizedState=t.baseState=e,e={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:pr,lastRenderedState:e},t.queue=e,e=e.dispatch=Zp.bind(null,W,e),[t.memoizedState,e]}function mr(e,t,n,r){return e={tag:e,create:t,destroy:n,deps:r,next:null},t=W.updateQueue,t===null?(t={lastEffect:null,stores:null},W.updateQueue=t,t.lastEffect=e.next=e):(n=t.lastEffect,n===null?t.lastEffect=e.next=e:(r=n.next,n.next=e,e.next=r,t.lastEffect=e)),e}function Dc(){return Me().memoizedState}function ei(e,t,n,r){var i=Ye();W.flags|=e,i.memoizedState=mr(1|t,n,void 0,r===void 0?null:r)}function Ui(e,t,n,r){var i=Me();r=r===void 0?null:r;var l=void 0;if(X!==null){var o=X.memoizedState;if(l=o.destroy,r!==null&&us(r,o.deps)){i.memoizedState=mr(t,n,l,r);return}}W.flags|=e,i.memoizedState=mr(1|t,n,l,r)}function xa(e,t){return ei(8390656,8,e,t)}function fs(e,t){return Ui(2048,8,e,t)}function Uc(e,t){return Ui(4,2,e,t)}function Bc(e,t){return Ui(4,4,e,t)}function $c(e,t){if(typeof t=="function")return e=e(),t(e),function(){t(null)};if(t!=null)return e=e(),t.current=e,function(){t.current=null}}function Hc(e,t,n){return n=n!=null?n.concat([e]):null,Ui(4,4,$c.bind(null,t,e),n)}function ps(){}function Vc(e,t){var n=Me();t=t===void 0?null:t;var r=n.memoizedState;return r!==null&&t!==null&&us(t,r[1])?r[0]:(n.memoizedState=[e,t],e)}function Wc(e,t){var n=Me();t=t===void 0?null:t;var r=n.memoizedState;return r!==null&&t!==null&&us(t,r[1])?r[0]:(e=e(),n.memoizedState=[e,t],e)}function Kc(e,t,n){return Ht&21?(Ve(n,t)||(n=Xu(),W.lanes|=n,Vt|=n,e.baseState=!0),t):(e.baseState&&(e.baseState=!1,ye=!0),e.memoizedState=n)}function Xp(e,t){var n=F;F=n!==0&&4>n?n:4,e(!0);var r=Sl.transition;Sl.transition={};try{e(!1),t()}finally{F=n,Sl.transition=r}}function Qc(){return Me().memoizedState}function Jp(e,t,n){var r=Nt(e);if(n={lane:r,action:n,hasEagerState:!1,eagerState:null,next:null},Gc(e))qc(t,n);else if(n=Tc(e,t,n,r),n!==null){var i=de();He(n,e,r,i),Yc(n,t,r)}}function Zp(e,t,n){var r=Nt(e),i={lane:r,action:n,hasEagerState:!1,eagerState:null,next:null};if(Gc(e))qc(t,i);else{var l=e.alternate;if(e.lanes===0&&(l===null||l.lanes===0)&&(l=t.lastRenderedReducer,l!==null))try{var o=t.lastRenderedState,s=l(o,n);if(i.hasEagerState=!0,i.eagerState=s,Ve(s,o)){var a=t.interleaved;a===null?(i.next=i,is(t)):(i.next=a.next,a.next=i),t.interleaved=i;return}}catch{}finally{}n=Tc(e,t,i,r),n!==null&&(i=de(),He(n,e,r,i),Yc(n,t,r))}}function Gc(e){var t=e.alternate;return e===W||t!==null&&t===W}function qc(e,t){qn=ji=!0;var n=e.pending;n===null?t.next=t:(t.next=n.next,n.next=t),e.pending=t}function Yc(e,t,n){if(n&4194240){var r=t.lanes;r&=e.pendingLanes,n|=r,t.lanes=n,Vo(e,n)}}var Ci={readContext:Ae,useCallback:ie,useContext:ie,useEffect:ie,useImperativeHandle:ie,useInsertionEffect:ie,useLayoutEffect:ie,useMemo:ie,useReducer:ie,useRef:ie,useState:ie,useDebugValue:ie,useDeferredValue:ie,useTransition:ie,useMutableSource:ie,useSyncExternalStore:ie,useId:ie,unstable_isNewReconciler:!1},em={readContext:Ae,useCallback:function(e,t){return Ye().memoizedState=[e,t===void 0?null:t],e},useContext:Ae,useEffect:xa,useImperativeHandle:function(e,t,n){return n=n!=null?n.concat([e]):null,ei(4194308,4,$c.bind(null,t,e),n)},useLayoutEffect:function(e,t){return ei(4194308,4,e,t)},useInsertionEffect:function(e,t){return ei(4,2,e,t)},useMemo:function(e,t){var n=Ye();return t=t===void 0?null:t,e=e(),n.memoizedState=[e,t],e},useReducer:function(e,t,n){var r=Ye();return t=n!==void 0?n(t):t,r.memoizedState=r.baseState=t,e={pending:null,interleaved:null,lanes:0,dispatch:null,lastRenderedReducer:e,lastRenderedState:t},r.queue=e,e=e.dispatch=Jp.bind(null,W,e),[r.memoizedState,e]},useRef:function(e){var t=Ye();return e={current:e},t.memoizedState=e},useState:va,useDebugValue:ps,useDeferredValue:function(e){return Ye().memoizedState=e},useTransition:function(){var e=va(!1),t=e[0];return e=Xp.bind(null,e[1]),Ye().memoizedState=e,[t,e]},useMutableSource:function(){},useSyncExternalStore:function(e,t,n){var r=W,i=Ye();if(H){if(n===void 0)throw Error(E(407));n=n()}else{if(n=t(),ee===null)throw Error(E(349));Ht&30||Lc(r,t,n)}i.memoizedState=n;var l={value:n,getSnapshot:t};return i.queue=l,xa(Mc.bind(null,r,l,e),[e]),r.flags|=2048,mr(9,Ac.bind(null,r,l,n,t),void 0,null),n},useId:function(){var e=Ye(),t=ee.identifierPrefix;if(H){var n=rt,r=nt;n=(r&~(1<<32-$e(r)-1)).toString(32)+n,t=":"+t+"R"+n,n=fr++,0<n&&(t+="H"+n.toString(32)),t+=":"}else n=Yp++,t=":"+t+"r"+n.toString(32)+":";return e.memoizedState=t},unstable_isNewReconciler:!1},tm={readContext:Ae,useCallback:Vc,useContext:Ae,useEffect:fs,useImperativeHandle:Hc,useInsertionEffect:Uc,useLayoutEffect:Bc,useMemo:Wc,useReducer:kl,useRef:Dc,useState:function(){return kl(pr)},useDebugValue:ps,useDeferredValue:function(e){var t=Me();return Kc(t,X.memoizedState,e)},useTransition:function(){var e=kl(pr)[0],t=Me().memoizedState;return[e,t]},useMutableSource:zc,useSyncExternalStore:Oc,useId:Qc,unstable_isNewReconciler:!1},nm={readContext:Ae,useCallback:Vc,useContext:Ae,useEffect:fs,useImperativeHandle:Hc,useInsertionEffect:Uc,useLayoutEffect:Bc,useMemo:Wc,useReducer:El,useRef:Dc,useState:function(){return El(pr)},useDebugValue:ps,useDeferredValue:function(e){var t=Me();return X===null?t.memoizedState=e:Kc(t,X.memoizedState,e)},useTransition:function(){var e=El(pr)[0],t=Me().memoizedState;return[e,t]},useMutableSource:zc,useSyncExternalStore:Oc,useId:Qc,unstable_isNewReconciler:!1};function De(e,t){if(e&&e.defaultProps){t=K({},t),e=e.defaultProps;for(var n in e)t[n]===void 0&&(t[n]=e[n]);return t}return t}function uo(e,t,n,r){t=e.memoizedState,n=n(r,t),n=n==null?t:K({},t,n),e.memoizedState=n,e.lanes===0&&(e.updateQueue.baseState=n)}var Bi={isMounted:function(e){return(e=e._reactInternals)?Gt(e)===e:!1},enqueueSetState:function(e,t,n){e=e._reactInternals;var r=de(),i=Nt(e),l=it(r,i);l.payload=t,n!=null&&(l.callback=n),t=kt(e,l,i),t!==null&&(He(t,e,i,r),Jr(t,e,i))},enqueueReplaceState:function(e,t,n){e=e._reactInternals;var r=de(),i=Nt(e),l=it(r,i);l.tag=1,l.payload=t,n!=null&&(l.callback=n),t=kt(e,l,i),t!==null&&(He(t,e,i,r),Jr(t,e,i))},enqueueForceUpdate:function(e,t){e=e._reactInternals;var n=de(),r=Nt(e),i=it(n,r);i.tag=2,t!=null&&(i.callback=t),t=kt(e,i,r),t!==null&&(He(t,e,r,n),Jr(t,e,r))}};function wa(e,t,n,r,i,l,o){return e=e.stateNode,typeof e.shouldComponentUpdate=="function"?e.shouldComponentUpdate(r,l,o):t.prototype&&t.prototype.isPureReactComponent?!or(n,r)||!or(i,l):!0}function Xc(e,t,n){var r=!1,i=_t,l=t.contextType;return typeof l=="object"&&l!==null?l=Ae(l):(i=xe(t)?Bt:ue.current,r=t.contextTypes,l=(r=r!=null)?vn(e,i):_t),t=new t(n,l),e.memoizedState=t.state!==null&&t.state!==void 0?t.state:null,t.updater=Bi,e.stateNode=t,t._reactInternals=e,r&&(e=e.stateNode,e.__reactInternalMemoizedUnmaskedChildContext=i,e.__reactInternalMemoizedMaskedChildContext=l),t}function Sa(e,t,n,r){e=t.state,typeof t.componentWillReceiveProps=="function"&&t.componentWillReceiveProps(n,r),typeof t.UNSAFE_componentWillReceiveProps=="function"&&t.UNSAFE_componentWillReceiveProps(n,r),t.state!==e&&Bi.enqueueReplaceState(t,t.state,null)}function co(e,t,n,r){var i=e.stateNode;i.props=n,i.state=e.memoizedState,i.refs={},ls(e);var l=t.contextType;typeof l=="object"&&l!==null?i.context=Ae(l):(l=xe(t)?Bt:ue.current,i.context=vn(e,l)),i.state=e.memoizedState,l=t.getDerivedStateFromProps,typeof l=="function"&&(uo(e,t,l,n),i.state=e.memoizedState),typeof t.getDerivedStateFromProps=="function"||typeof i.getSnapshotBeforeUpdate=="function"||typeof i.UNSAFE_componentWillMount!="function"&&typeof i.componentWillMount!="function"||(t=i.state,typeof i.componentWillMount=="function"&&i.componentWillMount(),typeof i.UNSAFE_componentWillMount=="function"&&i.UNSAFE_componentWillMount(),t!==i.state&&Bi.enqueueReplaceState(i,i.state,null),Ei(e,n,i,r),i.state=e.memoizedState),typeof i.componentDidMount=="function"&&(e.flags|=4194308)}function kn(e,t){try{var n="",r=t;do n+=bf(r),r=r.return;while(r);var i=n}catch(l){i=`
Error generating stack: `+l.message+`
`+l.stack}return{value:e,source:t,stack:i,digest:null}}function Nl(e,t,n){return{value:e,source:null,stack:n??null,digest:t??null}}function fo(e,t){try{console.error(t.value)}catch(n){setTimeout(function(){throw n})}}var rm=typeof WeakMap=="function"?WeakMap:Map;function Jc(e,t,n){n=it(-1,n),n.tag=3,n.payload={element:null};var r=t.value;return n.callback=function(){Ri||(Ri=!0,ko=r),fo(e,t)},n}function Zc(e,t,n){n=it(-1,n),n.tag=3;var r=e.type.getDerivedStateFromError;if(typeof r=="function"){var i=t.value;n.payload=function(){return r(i)},n.callback=function(){fo(e,t)}}var l=e.stateNode;return l!==null&&typeof l.componentDidCatch=="function"&&(n.callback=function(){fo(e,t),typeof r!="function"&&(Et===null?Et=new Set([this]):Et.add(this));var o=t.stack;this.componentDidCatch(t.value,{componentStack:o!==null?o:""})}),n}function ka(e,t,n){var r=e.pingCache;if(r===null){r=e.pingCache=new rm;var i=new Set;r.set(t,i)}else i=r.get(t),i===void 0&&(i=new Set,r.set(t,i));i.has(n)||(i.add(n),e=ym.bind(null,e,t,n),t.then(e,e))}function Ea(e){do{var t;if((t=e.tag===13)&&(t=e.memoizedState,t=t!==null?t.dehydrated!==null:!0),t)return e;e=e.return}while(e!==null);return null}function Na(e,t,n,r,i){return e.mode&1?(e.flags|=65536,e.lanes=i,e):(e===t?e.flags|=65536:(e.flags|=128,n.flags|=131072,n.flags&=-52805,n.tag===1&&(n.alternate===null?n.tag=17:(t=it(-1,1),t.tag=2,kt(n,t,1))),n.lanes|=1),e)}var im=ut.ReactCurrentOwner,ye=!1;function ce(e,t,n,r){t.child=e===null?Rc(t,null,n,r):wn(t,e.child,n,r)}function ja(e,t,n,r,i){n=n.render;var l=t.ref;return hn(t,i),r=cs(e,t,n,r,l,i),n=ds(),e!==null&&!ye?(t.updateQueue=e.updateQueue,t.flags&=-2053,e.lanes&=~i,at(e,t,i)):(H&&n&&Jo(t),t.flags|=1,ce(e,t,r,i),t.child)}function Ca(e,t,n,r,i){if(e===null){var l=n.type;return typeof l=="function"&&!Ss(l)&&l.defaultProps===void 0&&n.compare===null&&n.defaultProps===void 0?(t.tag=15,t.type=l,ed(e,t,l,r,i)):(e=ii(n.type,null,r,t,t.mode,i),e.ref=t.ref,e.return=t,t.child=e)}if(l=e.child,!(e.lanes&i)){var o=l.memoizedProps;if(n=n.compare,n=n!==null?n:or,n(o,r)&&e.ref===t.ref)return at(e,t,i)}return t.flags|=1,e=jt(l,r),e.ref=t.ref,e.return=t,t.child=e}function ed(e,t,n,r,i){if(e!==null){var l=e.memoizedProps;if(or(l,r)&&e.ref===t.ref)if(ye=!1,t.pendingProps=r=l,(e.lanes&i)!==0)e.flags&131072&&(ye=!0);else return t.lanes=e.lanes,at(e,t,i)}return po(e,t,n,r,i)}function td(e,t,n){var r=t.pendingProps,i=r.children,l=e!==null?e.memoizedState:null;if(r.mode==="hidden")if(!(t.mode&1))t.memoizedState={baseLanes:0,cachePool:null,transitions:null},D(cn,Ee),Ee|=n;else{if(!(n&1073741824))return e=l!==null?l.baseLanes|n:n,t.lanes=t.childLanes=1073741824,t.memoizedState={baseLanes:e,cachePool:null,transitions:null},t.updateQueue=null,D(cn,Ee),Ee|=e,null;t.memoizedState={baseLanes:0,cachePool:null,transitions:null},r=l!==null?l.baseLanes:n,D(cn,Ee),Ee|=r}else l!==null?(r=l.baseLanes|n,t.memoizedState=null):r=n,D(cn,Ee),Ee|=r;return ce(e,t,i,n),t.child}function nd(e,t){var n=t.ref;(e===null&&n!==null||e!==null&&e.ref!==n)&&(t.flags|=512,t.flags|=2097152)}function po(e,t,n,r,i){var l=xe(n)?Bt:ue.current;return l=vn(t,l),hn(t,i),n=cs(e,t,n,r,l,i),r=ds(),e!==null&&!ye?(t.updateQueue=e.updateQueue,t.flags&=-2053,e.lanes&=~i,at(e,t,i)):(H&&r&&Jo(t),t.flags|=1,ce(e,t,n,i),t.child)}function _a(e,t,n,r,i){if(xe(n)){var l=!0;vi(t)}else l=!1;if(hn(t,i),t.stateNode===null)ti(e,t),Xc(t,n,r),co(t,n,r,i),r=!0;else if(e===null){var o=t.stateNode,s=t.memoizedProps;o.props=s;var a=o.context,c=n.contextType;typeof c=="object"&&c!==null?c=Ae(c):(c=xe(n)?Bt:ue.current,c=vn(t,c));var f=n.getDerivedStateFromProps,d=typeof f=="function"||typeof o.getSnapshotBeforeUpdate=="function";d||typeof o.UNSAFE_componentWillReceiveProps!="function"&&typeof o.componentWillReceiveProps!="function"||(s!==r||a!==c)&&Sa(t,o,r,c),pt=!1;var h=t.memoizedState;o.state=h,Ei(t,r,o,i),a=t.memoizedState,s!==r||h!==a||ve.current||pt?(typeof f=="function"&&(uo(t,n,f,r),a=t.memoizedState),(s=pt||wa(t,n,s,r,h,a,c))?(d||typeof o.UNSAFE_componentWillMount!="function"&&typeof o.componentWillMount!="function"||(typeof o.componentWillMount=="function"&&o.componentWillMount(),typeof o.UNSAFE_componentWillMount=="function"&&o.UNSAFE_componentWillMount()),typeof o.componentDidMount=="function"&&(t.flags|=4194308)):(typeof o.componentDidMount=="function"&&(t.flags|=4194308),t.memoizedProps=r,t.memoizedState=a),o.props=r,o.state=a,o.context=c,r=s):(typeof o.componentDidMount=="function"&&(t.flags|=4194308),r=!1)}else{o=t.stateNode,bc(e,t),s=t.memoizedProps,c=t.type===t.elementType?s:De(t.type,s),o.props=c,d=t.pendingProps,h=o.context,a=n.contextType,typeof a=="object"&&a!==null?a=Ae(a):(a=xe(n)?Bt:ue.current,a=vn(t,a));var w=n.getDerivedStateFromProps;(f=typeof w=="function"||typeof o.getSnapshotBeforeUpdate=="function")||typeof o.UNSAFE_componentWillReceiveProps!="function"&&typeof o.componentWillReceiveProps!="function"||(s!==d||h!==a)&&Sa(t,o,r,a),pt=!1,h=t.memoizedState,o.state=h,Ei(t,r,o,i);var m=t.memoizedState;s!==d||h!==m||ve.current||pt?(typeof w=="function"&&(uo(t,n,w,r),m=t.memoizedState),(c=pt||wa(t,n,c,r,h,m,a)||!1)?(f||typeof o.UNSAFE_componentWillUpdate!="function"&&typeof o.componentWillUpdate!="function"||(typeof o.componentWillUpdate=="function"&&o.componentWillUpdate(r,m,a),typeof o.UNSAFE_componentWillUpdate=="function"&&o.UNSAFE_componentWillUpdate(r,m,a)),typeof o.componentDidUpdate=="function"&&(t.flags|=4),typeof o.getSnapshotBeforeUpdate=="function"&&(t.flags|=1024)):(typeof o.componentDidUpdate!="function"||s===e.memoizedProps&&h===e.memoizedState||(t.flags|=4),typeof o.getSnapshotBeforeUpdate!="function"||s===e.memoizedProps&&h===e.memoizedState||(t.flags|=1024),t.memoizedProps=r,t.memoizedState=m),o.props=r,o.state=m,o.context=a,r=c):(typeof o.componentDidUpdate!="function"||s===e.memoizedProps&&h===e.memoizedState||(t.flags|=4),typeof o.getSnapshotBeforeUpdate!="function"||s===e.memoizedProps&&h===e.memoizedState||(t.flags|=1024),r=!1)}return mo(e,t,n,r,l,i)}function mo(e,t,n,r,i,l){nd(e,t);var o=(t.flags&128)!==0;if(!r&&!o)return i&&fa(t,n,!1),at(e,t,l);r=t.stateNode,im.current=t;var s=o&&typeof n.getDerivedStateFromError!="function"?null:r.render();return t.flags|=1,e!==null&&o?(t.child=wn(t,e.child,null,l),t.child=wn(t,null,s,l)):ce(e,t,s,l),t.memoizedState=r.state,i&&fa(t,n,!0),t.child}function rd(e){var t=e.stateNode;t.pendingContext?da(e,t.pendingContext,t.pendingContext!==t.context):t.context&&da(e,t.context,!1),os(e,t.containerInfo)}function Ra(e,t,n,r,i){return xn(),es(i),t.flags|=256,ce(e,t,n,r),t.child}var ho={dehydrated:null,treeContext:null,retryLane:0};function go(e){return{baseLanes:e,cachePool:null,transitions:null}}function id(e,t,n){var r=t.pendingProps,i=V.current,l=!1,o=(t.flags&128)!==0,s;if((s=o)||(s=e!==null&&e.memoizedState===null?!1:(i&2)!==0),s?(l=!0,t.flags&=-129):(e===null||e.memoizedState!==null)&&(i|=1),D(V,i&1),e===null)return so(t),e=t.memoizedState,e!==null&&(e=e.dehydrated,e!==null)?(t.mode&1?e.data==="$!"?t.lanes=8:t.lanes=1073741824:t.lanes=1,null):(o=r.children,e=r.fallback,l?(r=t.mode,l=t.child,o={mode:"hidden",children:o},!(r&1)&&l!==null?(l.childLanes=0,l.pendingProps=o):l=Vi(o,r,0,null),e=Dt(e,r,n,null),l.return=t,e.return=t,l.sibling=e,t.child=l,t.child.memoizedState=go(n),t.memoizedState=ho,e):ms(t,o));if(i=e.memoizedState,i!==null&&(s=i.dehydrated,s!==null))return lm(e,t,o,r,s,i,n);if(l){l=r.fallback,o=t.mode,i=e.child,s=i.sibling;var a={mode:"hidden",children:r.children};return!(o&1)&&t.child!==i?(r=t.child,r.childLanes=0,r.pendingProps=a,t.deletions=null):(r=jt(i,a),r.subtreeFlags=i.subtreeFlags&14680064),s!==null?l=jt(s,l):(l=Dt(l,o,n,null),l.flags|=2),l.return=t,r.return=t,r.sibling=l,t.child=r,r=l,l=t.child,o=e.child.memoizedState,o=o===null?go(n):{baseLanes:o.baseLanes|n,cachePool:null,transitions:o.transitions},l.memoizedState=o,l.childLanes=e.childLanes&~n,t.memoizedState=ho,r}return l=e.child,e=l.sibling,r=jt(l,{mode:"visible",children:r.children}),!(t.mode&1)&&(r.lanes=n),r.return=t,r.sibling=null,e!==null&&(n=t.deletions,n===null?(t.deletions=[e],t.flags|=16):n.push(e)),t.child=r,t.memoizedState=null,r}function ms(e,t){return t=Vi({mode:"visible",children:t},e.mode,0,null),t.return=e,e.child=t}function $r(e,t,n,r){return r!==null&&es(r),wn(t,e.child,null,n),e=ms(t,t.pendingProps.children),e.flags|=2,t.memoizedState=null,e}function lm(e,t,n,r,i,l,o){if(n)return t.flags&256?(t.flags&=-257,r=Nl(Error(E(422))),$r(e,t,o,r)):t.memoizedState!==null?(t.child=e.child,t.flags|=128,null):(l=r.fallback,i=t.mode,r=Vi({mode:"visible",children:r.children},i,0,null),l=Dt(l,i,o,null),l.flags|=2,r.return=t,l.return=t,r.sibling=l,t.child=r,t.mode&1&&wn(t,e.child,null,o),t.child.memoizedState=go(o),t.memoizedState=ho,l);if(!(t.mode&1))return $r(e,t,o,null);if(i.data==="$!"){if(r=i.nextSibling&&i.nextSibling.dataset,r)var s=r.dgst;return r=s,l=Error(E(419)),r=Nl(l,r,void 0),$r(e,t,o,r)}if(s=(o&e.childLanes)!==0,ye||s){if(r=ee,r!==null){switch(o&-o){case 4:i=2;break;case 16:i=8;break;case 64:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:case 67108864:i=32;break;case 536870912:i=268435456;break;default:i=0}i=i&(r.suspendedLanes|o)?0:i,i!==0&&i!==l.retryLane&&(l.retryLane=i,st(e,i),He(r,e,i,-1))}return ws(),r=Nl(Error(E(421))),$r(e,t,o,r)}return i.data==="$?"?(t.flags|=128,t.child=e.child,t=vm.bind(null,e),i._reactRetry=t,null):(e=l.treeContext,Ne=St(i.nextSibling),Ce=t,H=!0,Be=null,e!==null&&(Pe[ze++]=nt,Pe[ze++]=rt,Pe[ze++]=$t,nt=e.id,rt=e.overflow,$t=t),t=ms(t,r.children),t.flags|=4096,t)}function Ta(e,t,n){e.lanes|=t;var r=e.alternate;r!==null&&(r.lanes|=t),ao(e.return,t,n)}function jl(e,t,n,r,i){var l=e.memoizedState;l===null?e.memoizedState={isBackwards:t,rendering:null,renderingStartTime:0,last:r,tail:n,tailMode:i}:(l.isBackwards=t,l.rendering=null,l.renderingStartTime=0,l.last=r,l.tail=n,l.tailMode=i)}function ld(e,t,n){var r=t.pendingProps,i=r.revealOrder,l=r.tail;if(ce(e,t,r.children,n),r=V.current,r&2)r=r&1|2,t.flags|=128;else{if(e!==null&&e.flags&128)e:for(e=t.child;e!==null;){if(e.tag===13)e.memoizedState!==null&&Ta(e,n,t);else if(e.tag===19)Ta(e,n,t);else if(e.child!==null){e.child.return=e,e=e.child;continue}if(e===t)break e;for(;e.sibling===null;){if(e.return===null||e.return===t)break e;e=e.return}e.sibling.return=e.return,e=e.sibling}r&=1}if(D(V,r),!(t.mode&1))t.memoizedState=null;else switch(i){case"forwards":for(n=t.child,i=null;n!==null;)e=n.alternate,e!==null&&Ni(e)===null&&(i=n),n=n.sibling;n=i,n===null?(i=t.child,t.child=null):(i=n.sibling,n.sibling=null),jl(t,!1,i,n,l);break;case"backwards":for(n=null,i=t.child,t.child=null;i!==null;){if(e=i.alternate,e!==null&&Ni(e)===null){t.child=i;break}e=i.sibling,i.sibling=n,n=i,i=e}jl(t,!0,n,null,l);break;case"together":jl(t,!1,null,null,void 0);break;default:t.memoizedState=null}return t.child}function ti(e,t){!(t.mode&1)&&e!==null&&(e.alternate=null,t.alternate=null,t.flags|=2)}function at(e,t,n){if(e!==null&&(t.dependencies=e.dependencies),Vt|=t.lanes,!(n&t.childLanes))return null;if(e!==null&&t.child!==e.child)throw Error(E(153));if(t.child!==null){for(e=t.child,n=jt(e,e.pendingProps),t.child=n,n.return=t;e.sibling!==null;)e=e.sibling,n=n.sibling=jt(e,e.pendingProps),n.return=t;n.sibling=null}return t.child}function om(e,t,n){switch(t.tag){case 3:rd(t),xn();break;case 5:Pc(t);break;case 1:xe(t.type)&&vi(t);break;case 4:os(t,t.stateNode.containerInfo);break;case 10:var r=t.type._context,i=t.memoizedProps.value;D(Si,r._currentValue),r._currentValue=i;break;case 13:if(r=t.memoizedState,r!==null)return r.dehydrated!==null?(D(V,V.current&1),t.flags|=128,null):n&t.child.childLanes?id(e,t,n):(D(V,V.current&1),e=at(e,t,n),e!==null?e.sibling:null);D(V,V.current&1);break;case 19:if(r=(n&t.childLanes)!==0,e.flags&128){if(r)return ld(e,t,n);t.flags|=128}if(i=t.memoizedState,i!==null&&(i.rendering=null,i.tail=null,i.lastEffect=null),D(V,V.current),r)break;return null;case 22:case 23:return t.lanes=0,td(e,t,n)}return at(e,t,n)}var od,yo,sd,ad;od=function(e,t){for(var n=t.child;n!==null;){if(n.tag===5||n.tag===6)e.appendChild(n.stateNode);else if(n.tag!==4&&n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return;n=n.return}n.sibling.return=n.return,n=n.sibling}};yo=function(){};sd=function(e,t,n,r){var i=e.memoizedProps;if(i!==r){e=t.stateNode,Mt(Ze.current);var l=null;switch(n){case"input":i=Il(e,i),r=Il(e,r),l=[];break;case"select":i=K({},i,{value:void 0}),r=K({},r,{value:void 0}),l=[];break;case"textarea":i=Bl(e,i),r=Bl(e,r),l=[];break;default:typeof i.onClick!="function"&&typeof r.onClick=="function"&&(e.onclick=gi)}Hl(n,r);var o;n=null;for(c in i)if(!r.hasOwnProperty(c)&&i.hasOwnProperty(c)&&i[c]!=null)if(c==="style"){var s=i[c];for(o in s)s.hasOwnProperty(o)&&(n||(n={}),n[o]="")}else c!=="dangerouslySetInnerHTML"&&c!=="children"&&c!=="suppressContentEditableWarning"&&c!=="suppressHydrationWarning"&&c!=="autoFocus"&&(Zn.hasOwnProperty(c)?l||(l=[]):(l=l||[]).push(c,null));for(c in r){var a=r[c];if(s=i!=null?i[c]:void 0,r.hasOwnProperty(c)&&a!==s&&(a!=null||s!=null))if(c==="style")if(s){for(o in s)!s.hasOwnProperty(o)||a&&a.hasOwnProperty(o)||(n||(n={}),n[o]="");for(o in a)a.hasOwnProperty(o)&&s[o]!==a[o]&&(n||(n={}),n[o]=a[o])}else n||(l||(l=[]),l.push(c,n)),n=a;else c==="dangerouslySetInnerHTML"?(a=a?a.__html:void 0,s=s?s.__html:void 0,a!=null&&s!==a&&(l=l||[]).push(c,a)):c==="children"?typeof a!="string"&&typeof a!="number"||(l=l||[]).push(c,""+a):c!=="suppressContentEditableWarning"&&c!=="suppressHydrationWarning"&&(Zn.hasOwnProperty(c)?(a!=null&&c==="onScroll"&&B("scroll",e),l||s===a||(l=[])):(l=l||[]).push(c,a))}n&&(l=l||[]).push("style",n);var c=l;(t.updateQueue=c)&&(t.flags|=4)}};ad=function(e,t,n,r){n!==r&&(t.flags|=4)};function Fn(e,t){if(!H)switch(e.tailMode){case"hidden":t=e.tail;for(var n=null;t!==null;)t.alternate!==null&&(n=t),t=t.sibling;n===null?e.tail=null:n.sibling=null;break;case"collapsed":n=e.tail;for(var r=null;n!==null;)n.alternate!==null&&(r=n),n=n.sibling;r===null?t||e.tail===null?e.tail=null:e.tail.sibling=null:r.sibling=null}}function le(e){var t=e.alternate!==null&&e.alternate.child===e.child,n=0,r=0;if(t)for(var i=e.child;i!==null;)n|=i.lanes|i.childLanes,r|=i.subtreeFlags&14680064,r|=i.flags&14680064,i.return=e,i=i.sibling;else for(i=e.child;i!==null;)n|=i.lanes|i.childLanes,r|=i.subtreeFlags,r|=i.flags,i.return=e,i=i.sibling;return e.subtreeFlags|=r,e.childLanes=n,t}function sm(e,t,n){var r=t.pendingProps;switch(Zo(t),t.tag){case 2:case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return le(t),null;case 1:return xe(t.type)&&yi(),le(t),null;case 3:return r=t.stateNode,Sn(),$(ve),$(ue),as(),r.pendingContext&&(r.context=r.pendingContext,r.pendingContext=null),(e===null||e.child===null)&&(Ur(t)?t.flags|=4:e===null||e.memoizedState.isDehydrated&&!(t.flags&256)||(t.flags|=1024,Be!==null&&(jo(Be),Be=null))),yo(e,t),le(t),null;case 5:ss(t);var i=Mt(dr.current);if(n=t.type,e!==null&&t.stateNode!=null)sd(e,t,n,r,i),e.ref!==t.ref&&(t.flags|=512,t.flags|=2097152);else{if(!r){if(t.stateNode===null)throw Error(E(166));return le(t),null}if(e=Mt(Ze.current),Ur(t)){r=t.stateNode,n=t.type;var l=t.memoizedProps;switch(r[Xe]=t,r[ur]=l,e=(t.mode&1)!==0,n){case"dialog":B("cancel",r),B("close",r);break;case"iframe":case"object":case"embed":B("load",r);break;case"video":case"audio":for(i=0;i<Hn.length;i++)B(Hn[i],r);break;case"source":B("error",r);break;case"img":case"image":case"link":B("error",r),B("load",r);break;case"details":B("toggle",r);break;case"input":Is(r,l),B("invalid",r);break;case"select":r._wrapperState={wasMultiple:!!l.multiple},B("invalid",r);break;case"textarea":Us(r,l),B("invalid",r)}Hl(n,l),i=null;for(var o in l)if(l.hasOwnProperty(o)){var s=l[o];o==="children"?typeof s=="string"?r.textContent!==s&&(l.suppressHydrationWarning!==!0&&Dr(r.textContent,s,e),i=["children",s]):typeof s=="number"&&r.textContent!==""+s&&(l.suppressHydrationWarning!==!0&&Dr(r.textContent,s,e),i=["children",""+s]):Zn.hasOwnProperty(o)&&s!=null&&o==="onScroll"&&B("scroll",r)}switch(n){case"input":Pr(r),Ds(r,l,!0);break;case"textarea":Pr(r),Bs(r);break;case"select":case"option":break;default:typeof l.onClick=="function"&&(r.onclick=gi)}r=i,t.updateQueue=r,r!==null&&(t.flags|=4)}else{o=i.nodeType===9?i:i.ownerDocument,e==="http://www.w3.org/1999/xhtml"&&(e=Mu(n)),e==="http://www.w3.org/1999/xhtml"?n==="script"?(e=o.createElement("div"),e.innerHTML="<script><\/script>",e=e.removeChild(e.firstChild)):typeof r.is=="string"?e=o.createElement(n,{is:r.is}):(e=o.createElement(n),n==="select"&&(o=e,r.multiple?o.multiple=!0:r.size&&(o.size=r.size))):e=o.createElementNS(e,n),e[Xe]=t,e[ur]=r,od(e,t,!1,!1),t.stateNode=e;e:{switch(o=Vl(n,r),n){case"dialog":B("cancel",e),B("close",e),i=r;break;case"iframe":case"object":case"embed":B("load",e),i=r;break;case"video":case"audio":for(i=0;i<Hn.length;i++)B(Hn[i],e);i=r;break;case"source":B("error",e),i=r;break;case"img":case"image":case"link":B("error",e),B("load",e),i=r;break;case"details":B("toggle",e),i=r;break;case"input":Is(e,r),i=Il(e,r),B("invalid",e);break;case"option":i=r;break;case"select":e._wrapperState={wasMultiple:!!r.multiple},i=K({},r,{value:void 0}),B("invalid",e);break;case"textarea":Us(e,r),i=Bl(e,r),B("invalid",e);break;default:i=r}Hl(n,i),s=i;for(l in s)if(s.hasOwnProperty(l)){var a=s[l];l==="style"?Du(e,a):l==="dangerouslySetInnerHTML"?(a=a?a.__html:void 0,a!=null&&Fu(e,a)):l==="children"?typeof a=="string"?(n!=="textarea"||a!=="")&&er(e,a):typeof a=="number"&&er(e,""+a):l!=="suppressContentEditableWarning"&&l!=="suppressHydrationWarning"&&l!=="autoFocus"&&(Zn.hasOwnProperty(l)?a!=null&&l==="onScroll"&&B("scroll",e):a!=null&&Io(e,l,a,o))}switch(n){case"input":Pr(e),Ds(e,r,!1);break;case"textarea":Pr(e),Bs(e);break;case"option":r.value!=null&&e.setAttribute("value",""+Ct(r.value));break;case"select":e.multiple=!!r.multiple,l=r.value,l!=null?dn(e,!!r.multiple,l,!1):r.defaultValue!=null&&dn(e,!!r.multiple,r.defaultValue,!0);break;default:typeof i.onClick=="function"&&(e.onclick=gi)}switch(n){case"button":case"input":case"select":case"textarea":r=!!r.autoFocus;break e;case"img":r=!0;break e;default:r=!1}}r&&(t.flags|=4)}t.ref!==null&&(t.flags|=512,t.flags|=2097152)}return le(t),null;case 6:if(e&&t.stateNode!=null)ad(e,t,e.memoizedProps,r);else{if(typeof r!="string"&&t.stateNode===null)throw Error(E(166));if(n=Mt(dr.current),Mt(Ze.current),Ur(t)){if(r=t.stateNode,n=t.memoizedProps,r[Xe]=t,(l=r.nodeValue!==n)&&(e=Ce,e!==null))switch(e.tag){case 3:Dr(r.nodeValue,n,(e.mode&1)!==0);break;case 5:e.memoizedProps.suppressHydrationWarning!==!0&&Dr(r.nodeValue,n,(e.mode&1)!==0)}l&&(t.flags|=4)}else r=(n.nodeType===9?n:n.ownerDocument).createTextNode(r),r[Xe]=t,t.stateNode=r}return le(t),null;case 13:if($(V),r=t.memoizedState,e===null||e.memoizedState!==null&&e.memoizedState.dehydrated!==null){if(H&&Ne!==null&&t.mode&1&&!(t.flags&128))Cc(),xn(),t.flags|=98560,l=!1;else if(l=Ur(t),r!==null&&r.dehydrated!==null){if(e===null){if(!l)throw Error(E(318));if(l=t.memoizedState,l=l!==null?l.dehydrated:null,!l)throw Error(E(317));l[Xe]=t}else xn(),!(t.flags&128)&&(t.memoizedState=null),t.flags|=4;le(t),l=!1}else Be!==null&&(jo(Be),Be=null),l=!0;if(!l)return t.flags&65536?t:null}return t.flags&128?(t.lanes=n,t):(r=r!==null,r!==(e!==null&&e.memoizedState!==null)&&r&&(t.child.flags|=8192,t.mode&1&&(e===null||V.current&1?J===0&&(J=3):ws())),t.updateQueue!==null&&(t.flags|=4),le(t),null);case 4:return Sn(),yo(e,t),e===null&&sr(t.stateNode.containerInfo),le(t),null;case 10:return rs(t.type._context),le(t),null;case 17:return xe(t.type)&&yi(),le(t),null;case 19:if($(V),l=t.memoizedState,l===null)return le(t),null;if(r=(t.flags&128)!==0,o=l.rendering,o===null)if(r)Fn(l,!1);else{if(J!==0||e!==null&&e.flags&128)for(e=t.child;e!==null;){if(o=Ni(e),o!==null){for(t.flags|=128,Fn(l,!1),r=o.updateQueue,r!==null&&(t.updateQueue=r,t.flags|=4),t.subtreeFlags=0,r=n,n=t.child;n!==null;)l=n,e=r,l.flags&=14680066,o=l.alternate,o===null?(l.childLanes=0,l.lanes=e,l.child=null,l.subtreeFlags=0,l.memoizedProps=null,l.memoizedState=null,l.updateQueue=null,l.dependencies=null,l.stateNode=null):(l.childLanes=o.childLanes,l.lanes=o.lanes,l.child=o.child,l.subtreeFlags=0,l.deletions=null,l.memoizedProps=o.memoizedProps,l.memoizedState=o.memoizedState,l.updateQueue=o.updateQueue,l.type=o.type,e=o.dependencies,l.dependencies=e===null?null:{lanes:e.lanes,firstContext:e.firstContext}),n=n.sibling;return D(V,V.current&1|2),t.child}e=e.sibling}l.tail!==null&&G()>En&&(t.flags|=128,r=!0,Fn(l,!1),t.lanes=4194304)}else{if(!r)if(e=Ni(o),e!==null){if(t.flags|=128,r=!0,n=e.updateQueue,n!==null&&(t.updateQueue=n,t.flags|=4),Fn(l,!0),l.tail===null&&l.tailMode==="hidden"&&!o.alternate&&!H)return le(t),null}else 2*G()-l.renderingStartTime>En&&n!==1073741824&&(t.flags|=128,r=!0,Fn(l,!1),t.lanes=4194304);l.isBackwards?(o.sibling=t.child,t.child=o):(n=l.last,n!==null?n.sibling=o:t.child=o,l.last=o)}return l.tail!==null?(t=l.tail,l.rendering=t,l.tail=t.sibling,l.renderingStartTime=G(),t.sibling=null,n=V.current,D(V,r?n&1|2:n&1),t):(le(t),null);case 22:case 23:return xs(),r=t.memoizedState!==null,e!==null&&e.memoizedState!==null!==r&&(t.flags|=8192),r&&t.mode&1?Ee&1073741824&&(le(t),t.subtreeFlags&6&&(t.flags|=8192)):le(t),null;case 24:return null;case 25:return null}throw Error(E(156,t.tag))}function am(e,t){switch(Zo(t),t.tag){case 1:return xe(t.type)&&yi(),e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 3:return Sn(),$(ve),$(ue),as(),e=t.flags,e&65536&&!(e&128)?(t.flags=e&-65537|128,t):null;case 5:return ss(t),null;case 13:if($(V),e=t.memoizedState,e!==null&&e.dehydrated!==null){if(t.alternate===null)throw Error(E(340));xn()}return e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 19:return $(V),null;case 4:return Sn(),null;case 10:return rs(t.type._context),null;case 22:case 23:return xs(),null;case 24:return null;default:return null}}var Hr=!1,oe=!1,um=typeof WeakSet=="function"?WeakSet:Set,_=null;function un(e,t){var n=e.ref;if(n!==null)if(typeof n=="function")try{n(null)}catch(r){Q(e,t,r)}else n.current=null}function vo(e,t,n){try{n()}catch(r){Q(e,t,r)}}var ba=!1;function cm(e,t){if(eo=pi,e=pc(),Xo(e)){if("selectionStart"in e)var n={start:e.selectionStart,end:e.selectionEnd};else e:{n=(n=e.ownerDocument)&&n.defaultView||window;var r=n.getSelection&&n.getSelection();if(r&&r.rangeCount!==0){n=r.anchorNode;var i=r.anchorOffset,l=r.focusNode;r=r.focusOffset;try{n.nodeType,l.nodeType}catch{n=null;break e}var o=0,s=-1,a=-1,c=0,f=0,d=e,h=null;t:for(;;){for(var w;d!==n||i!==0&&d.nodeType!==3||(s=o+i),d!==l||r!==0&&d.nodeType!==3||(a=o+r),d.nodeType===3&&(o+=d.nodeValue.length),(w=d.firstChild)!==null;)h=d,d=w;for(;;){if(d===e)break t;if(h===n&&++c===i&&(s=o),h===l&&++f===r&&(a=o),(w=d.nextSibling)!==null)break;d=h,h=d.parentNode}d=w}n=s===-1||a===-1?null:{start:s,end:a}}else n=null}n=n||{start:0,end:0}}else n=null;for(to={focusedElem:e,selectionRange:n},pi=!1,_=t;_!==null;)if(t=_,e=t.child,(t.subtreeFlags&1028)!==0&&e!==null)e.return=t,_=e;else for(;_!==null;){t=_;try{var m=t.alternate;if(t.flags&1024)switch(t.tag){case 0:case 11:case 15:break;case 1:if(m!==null){var v=m.memoizedProps,k=m.memoizedState,g=t.stateNode,p=g.getSnapshotBeforeUpdate(t.elementType===t.type?v:De(t.type,v),k);g.__reactInternalSnapshotBeforeUpdate=p}break;case 3:var y=t.stateNode.containerInfo;y.nodeType===1?y.textContent="":y.nodeType===9&&y.documentElement&&y.removeChild(y.documentElement);break;case 5:case 6:case 4:case 17:break;default:throw Error(E(163))}}catch(S){Q(t,t.return,S)}if(e=t.sibling,e!==null){e.return=t.return,_=e;break}_=t.return}return m=ba,ba=!1,m}function Yn(e,t,n){var r=t.updateQueue;if(r=r!==null?r.lastEffect:null,r!==null){var i=r=r.next;do{if((i.tag&e)===e){var l=i.destroy;i.destroy=void 0,l!==void 0&&vo(t,n,l)}i=i.next}while(i!==r)}}function $i(e,t){if(t=t.updateQueue,t=t!==null?t.lastEffect:null,t!==null){var n=t=t.next;do{if((n.tag&e)===e){var r=n.create;n.destroy=r()}n=n.next}while(n!==t)}}function xo(e){var t=e.ref;if(t!==null){var n=e.stateNode;switch(e.tag){case 5:e=n;break;default:e=n}typeof t=="function"?t(e):t.current=e}}function ud(e){var t=e.alternate;t!==null&&(e.alternate=null,ud(t)),e.child=null,e.deletions=null,e.sibling=null,e.tag===5&&(t=e.stateNode,t!==null&&(delete t[Xe],delete t[ur],delete t[io],delete t[Kp],delete t[Qp])),e.stateNode=null,e.return=null,e.dependencies=null,e.memoizedProps=null,e.memoizedState=null,e.pendingProps=null,e.stateNode=null,e.updateQueue=null}function cd(e){return e.tag===5||e.tag===3||e.tag===4}function Pa(e){e:for(;;){for(;e.sibling===null;){if(e.return===null||cd(e.return))return null;e=e.return}for(e.sibling.return=e.return,e=e.sibling;e.tag!==5&&e.tag!==6&&e.tag!==18;){if(e.flags&2||e.child===null||e.tag===4)continue e;e.child.return=e,e=e.child}if(!(e.flags&2))return e.stateNode}}function wo(e,t,n){var r=e.tag;if(r===5||r===6)e=e.stateNode,t?n.nodeType===8?n.parentNode.insertBefore(e,t):n.insertBefore(e,t):(n.nodeType===8?(t=n.parentNode,t.insertBefore(e,n)):(t=n,t.appendChild(e)),n=n._reactRootContainer,n!=null||t.onclick!==null||(t.onclick=gi));else if(r!==4&&(e=e.child,e!==null))for(wo(e,t,n),e=e.sibling;e!==null;)wo(e,t,n),e=e.sibling}function So(e,t,n){var r=e.tag;if(r===5||r===6)e=e.stateNode,t?n.insertBefore(e,t):n.appendChild(e);else if(r!==4&&(e=e.child,e!==null))for(So(e,t,n),e=e.sibling;e!==null;)So(e,t,n),e=e.sibling}var te=null,Ue=!1;function dt(e,t,n){for(n=n.child;n!==null;)dd(e,t,n),n=n.sibling}function dd(e,t,n){if(Je&&typeof Je.onCommitFiberUnmount=="function")try{Je.onCommitFiberUnmount(Li,n)}catch{}switch(n.tag){case 5:oe||un(n,t);case 6:var r=te,i=Ue;te=null,dt(e,t,n),te=r,Ue=i,te!==null&&(Ue?(e=te,n=n.stateNode,e.nodeType===8?e.parentNode.removeChild(n):e.removeChild(n)):te.removeChild(n.stateNode));break;case 18:te!==null&&(Ue?(e=te,n=n.stateNode,e.nodeType===8?vl(e.parentNode,n):e.nodeType===1&&vl(e,n),ir(e)):vl(te,n.stateNode));break;case 4:r=te,i=Ue,te=n.stateNode.containerInfo,Ue=!0,dt(e,t,n),te=r,Ue=i;break;case 0:case 11:case 14:case 15:if(!oe&&(r=n.updateQueue,r!==null&&(r=r.lastEffect,r!==null))){i=r=r.next;do{var l=i,o=l.destroy;l=l.tag,o!==void 0&&(l&2||l&4)&&vo(n,t,o),i=i.next}while(i!==r)}dt(e,t,n);break;case 1:if(!oe&&(un(n,t),r=n.stateNode,typeof r.componentWillUnmount=="function"))try{r.props=n.memoizedProps,r.state=n.memoizedState,r.componentWillUnmount()}catch(s){Q(n,t,s)}dt(e,t,n);break;case 21:dt(e,t,n);break;case 22:n.mode&1?(oe=(r=oe)||n.memoizedState!==null,dt(e,t,n),oe=r):dt(e,t,n);break;default:dt(e,t,n)}}function za(e){var t=e.updateQueue;if(t!==null){e.updateQueue=null;var n=e.stateNode;n===null&&(n=e.stateNode=new um),t.forEach(function(r){var i=xm.bind(null,e,r);n.has(r)||(n.add(r),r.then(i,i))})}}function Ie(e,t){var n=t.deletions;if(n!==null)for(var r=0;r<n.length;r++){var i=n[r];try{var l=e,o=t,s=o;e:for(;s!==null;){switch(s.tag){case 5:te=s.stateNode,Ue=!1;break e;case 3:te=s.stateNode.containerInfo,Ue=!0;break e;case 4:te=s.stateNode.containerInfo,Ue=!0;break e}s=s.return}if(te===null)throw Error(E(160));dd(l,o,i),te=null,Ue=!1;var a=i.alternate;a!==null&&(a.return=null),i.return=null}catch(c){Q(i,t,c)}}if(t.subtreeFlags&12854)for(t=t.child;t!==null;)fd(t,e),t=t.sibling}function fd(e,t){var n=e.alternate,r=e.flags;switch(e.tag){case 0:case 11:case 14:case 15:if(Ie(t,e),Ge(e),r&4){try{Yn(3,e,e.return),$i(3,e)}catch(v){Q(e,e.return,v)}try{Yn(5,e,e.return)}catch(v){Q(e,e.return,v)}}break;case 1:Ie(t,e),Ge(e),r&512&&n!==null&&un(n,n.return);break;case 5:if(Ie(t,e),Ge(e),r&512&&n!==null&&un(n,n.return),e.flags&32){var i=e.stateNode;try{er(i,"")}catch(v){Q(e,e.return,v)}}if(r&4&&(i=e.stateNode,i!=null)){var l=e.memoizedProps,o=n!==null?n.memoizedProps:l,s=e.type,a=e.updateQueue;if(e.updateQueue=null,a!==null)try{s==="input"&&l.type==="radio"&&l.name!=null&&Lu(i,l),Vl(s,o);var c=Vl(s,l);for(o=0;o<a.length;o+=2){var f=a[o],d=a[o+1];f==="style"?Du(i,d):f==="dangerouslySetInnerHTML"?Fu(i,d):f==="children"?er(i,d):Io(i,f,d,c)}switch(s){case"input":Dl(i,l);break;case"textarea":Au(i,l);break;case"select":var h=i._wrapperState.wasMultiple;i._wrapperState.wasMultiple=!!l.multiple;var w=l.value;w!=null?dn(i,!!l.multiple,w,!1):h!==!!l.multiple&&(l.defaultValue!=null?dn(i,!!l.multiple,l.defaultValue,!0):dn(i,!!l.multiple,l.multiple?[]:"",!1))}i[ur]=l}catch(v){Q(e,e.return,v)}}break;case 6:if(Ie(t,e),Ge(e),r&4){if(e.stateNode===null)throw Error(E(162));i=e.stateNode,l=e.memoizedProps;try{i.nodeValue=l}catch(v){Q(e,e.return,v)}}break;case 3:if(Ie(t,e),Ge(e),r&4&&n!==null&&n.memoizedState.isDehydrated)try{ir(t.containerInfo)}catch(v){Q(e,e.return,v)}break;case 4:Ie(t,e),Ge(e);break;case 13:Ie(t,e),Ge(e),i=e.child,i.flags&8192&&(l=i.memoizedState!==null,i.stateNode.isHidden=l,!l||i.alternate!==null&&i.alternate.memoizedState!==null||(ys=G())),r&4&&za(e);break;case 22:if(f=n!==null&&n.memoizedState!==null,e.mode&1?(oe=(c=oe)||f,Ie(t,e),oe=c):Ie(t,e),Ge(e),r&8192){if(c=e.memoizedState!==null,(e.stateNode.isHidden=c)&&!f&&e.mode&1)for(_=e,f=e.child;f!==null;){for(d=_=f;_!==null;){switch(h=_,w=h.child,h.tag){case 0:case 11:case 14:case 15:Yn(4,h,h.return);break;case 1:un(h,h.return);var m=h.stateNode;if(typeof m.componentWillUnmount=="function"){r=h,n=h.return;try{t=r,m.props=t.memoizedProps,m.state=t.memoizedState,m.componentWillUnmount()}catch(v){Q(r,n,v)}}break;case 5:un(h,h.return);break;case 22:if(h.memoizedState!==null){La(d);continue}}w!==null?(w.return=h,_=w):La(d)}f=f.sibling}e:for(f=null,d=e;;){if(d.tag===5){if(f===null){f=d;try{i=d.stateNode,c?(l=i.style,typeof l.setProperty=="function"?l.setProperty("display","none","important"):l.display="none"):(s=d.stateNode,a=d.memoizedProps.style,o=a!=null&&a.hasOwnProperty("display")?a.display:null,s.style.display=Iu("display",o))}catch(v){Q(e,e.return,v)}}}else if(d.tag===6){if(f===null)try{d.stateNode.nodeValue=c?"":d.memoizedProps}catch(v){Q(e,e.return,v)}}else if((d.tag!==22&&d.tag!==23||d.memoizedState===null||d===e)&&d.child!==null){d.child.return=d,d=d.child;continue}if(d===e)break e;for(;d.sibling===null;){if(d.return===null||d.return===e)break e;f===d&&(f=null),d=d.return}f===d&&(f=null),d.sibling.return=d.return,d=d.sibling}}break;case 19:Ie(t,e),Ge(e),r&4&&za(e);break;case 21:break;default:Ie(t,e),Ge(e)}}function Ge(e){var t=e.flags;if(t&2){try{e:{for(var n=e.return;n!==null;){if(cd(n)){var r=n;break e}n=n.return}throw Error(E(160))}switch(r.tag){case 5:var i=r.stateNode;r.flags&32&&(er(i,""),r.flags&=-33);var l=Pa(e);So(e,l,i);break;case 3:case 4:var o=r.stateNode.containerInfo,s=Pa(e);wo(e,s,o);break;default:throw Error(E(161))}}catch(a){Q(e,e.return,a)}e.flags&=-3}t&4096&&(e.flags&=-4097)}function dm(e,t,n){_=e,pd(e)}function pd(e,t,n){for(var r=(e.mode&1)!==0;_!==null;){var i=_,l=i.child;if(i.tag===22&&r){var o=i.memoizedState!==null||Hr;if(!o){var s=i.alternate,a=s!==null&&s.memoizedState!==null||oe;s=Hr;var c=oe;if(Hr=o,(oe=a)&&!c)for(_=i;_!==null;)o=_,a=o.child,o.tag===22&&o.memoizedState!==null?Aa(i):a!==null?(a.return=o,_=a):Aa(i);for(;l!==null;)_=l,pd(l),l=l.sibling;_=i,Hr=s,oe=c}Oa(e)}else i.subtreeFlags&8772&&l!==null?(l.return=i,_=l):Oa(e)}}function Oa(e){for(;_!==null;){var t=_;if(t.flags&8772){var n=t.alternate;try{if(t.flags&8772)switch(t.tag){case 0:case 11:case 15:oe||$i(5,t);break;case 1:var r=t.stateNode;if(t.flags&4&&!oe)if(n===null)r.componentDidMount();else{var i=t.elementType===t.type?n.memoizedProps:De(t.type,n.memoizedProps);r.componentDidUpdate(i,n.memoizedState,r.__reactInternalSnapshotBeforeUpdate)}var l=t.updateQueue;l!==null&&ya(t,l,r);break;case 3:var o=t.updateQueue;if(o!==null){if(n=null,t.child!==null)switch(t.child.tag){case 5:n=t.child.stateNode;break;case 1:n=t.child.stateNode}ya(t,o,n)}break;case 5:var s=t.stateNode;if(n===null&&t.flags&4){n=s;var a=t.memoizedProps;switch(t.type){case"button":case"input":case"select":case"textarea":a.autoFocus&&n.focus();break;case"img":a.src&&(n.src=a.src)}}break;case 6:break;case 4:break;case 12:break;case 13:if(t.memoizedState===null){var c=t.alternate;if(c!==null){var f=c.memoizedState;if(f!==null){var d=f.dehydrated;d!==null&&ir(d)}}}break;case 19:case 17:case 21:case 22:case 23:case 25:break;default:throw Error(E(163))}oe||t.flags&512&&xo(t)}catch(h){Q(t,t.return,h)}}if(t===e){_=null;break}if(n=t.sibling,n!==null){n.return=t.return,_=n;break}_=t.return}}function La(e){for(;_!==null;){var t=_;if(t===e){_=null;break}var n=t.sibling;if(n!==null){n.return=t.return,_=n;break}_=t.return}}function Aa(e){for(;_!==null;){var t=_;try{switch(t.tag){case 0:case 11:case 15:var n=t.return;try{$i(4,t)}catch(a){Q(t,n,a)}break;case 1:var r=t.stateNode;if(typeof r.componentDidMount=="function"){var i=t.return;try{r.componentDidMount()}catch(a){Q(t,i,a)}}var l=t.return;try{xo(t)}catch(a){Q(t,l,a)}break;case 5:var o=t.return;try{xo(t)}catch(a){Q(t,o,a)}}}catch(a){Q(t,t.return,a)}if(t===e){_=null;break}var s=t.sibling;if(s!==null){s.return=t.return,_=s;break}_=t.return}}var fm=Math.ceil,_i=ut.ReactCurrentDispatcher,hs=ut.ReactCurrentOwner,Le=ut.ReactCurrentBatchConfig,A=0,ee=null,Y=null,ne=0,Ee=0,cn=Tt(0),J=0,hr=null,Vt=0,Hi=0,gs=0,Xn=null,ge=null,ys=0,En=1/0,et=null,Ri=!1,ko=null,Et=null,Vr=!1,yt=null,Ti=0,Jn=0,Eo=null,ni=-1,ri=0;function de(){return A&6?G():ni!==-1?ni:ni=G()}function Nt(e){return e.mode&1?A&2&&ne!==0?ne&-ne:qp.transition!==null?(ri===0&&(ri=Xu()),ri):(e=F,e!==0||(e=window.event,e=e===void 0?16:ic(e.type)),e):1}function He(e,t,n,r){if(50<Jn)throw Jn=0,Eo=null,Error(E(185));vr(e,n,r),(!(A&2)||e!==ee)&&(e===ee&&(!(A&2)&&(Hi|=n),J===4&&ht(e,ne)),we(e,r),n===1&&A===0&&!(t.mode&1)&&(En=G()+500,Di&&bt()))}function we(e,t){var n=e.callbackNode;qf(e,t);var r=fi(e,e===ee?ne:0);if(r===0)n!==null&&Vs(n),e.callbackNode=null,e.callbackPriority=0;else if(t=r&-r,e.callbackPriority!==t){if(n!=null&&Vs(n),t===1)e.tag===0?Gp(Ma.bind(null,e)):Ec(Ma.bind(null,e)),Vp(function(){!(A&6)&&bt()}),n=null;else{switch(Ju(r)){case 1:n=Ho;break;case 4:n=qu;break;case 16:n=di;break;case 536870912:n=Yu;break;default:n=di}n=Sd(n,md.bind(null,e))}e.callbackPriority=t,e.callbackNode=n}}function md(e,t){if(ni=-1,ri=0,A&6)throw Error(E(327));var n=e.callbackNode;if(gn()&&e.callbackNode!==n)return null;var r=fi(e,e===ee?ne:0);if(r===0)return null;if(r&30||r&e.expiredLanes||t)t=bi(e,r);else{t=r;var i=A;A|=2;var l=gd();(ee!==e||ne!==t)&&(et=null,En=G()+500,It(e,t));do try{hm();break}catch(s){hd(e,s)}while(!0);ns(),_i.current=l,A=i,Y!==null?t=0:(ee=null,ne=0,t=J)}if(t!==0){if(t===2&&(i=ql(e),i!==0&&(r=i,t=No(e,i))),t===1)throw n=hr,It(e,0),ht(e,r),we(e,G()),n;if(t===6)ht(e,r);else{if(i=e.current.alternate,!(r&30)&&!pm(i)&&(t=bi(e,r),t===2&&(l=ql(e),l!==0&&(r=l,t=No(e,l))),t===1))throw n=hr,It(e,0),ht(e,r),we(e,G()),n;switch(e.finishedWork=i,e.finishedLanes=r,t){case 0:case 1:throw Error(E(345));case 2:Ot(e,ge,et);break;case 3:if(ht(e,r),(r&130023424)===r&&(t=ys+500-G(),10<t)){if(fi(e,0)!==0)break;if(i=e.suspendedLanes,(i&r)!==r){de(),e.pingedLanes|=e.suspendedLanes&i;break}e.timeoutHandle=ro(Ot.bind(null,e,ge,et),t);break}Ot(e,ge,et);break;case 4:if(ht(e,r),(r&4194240)===r)break;for(t=e.eventTimes,i=-1;0<r;){var o=31-$e(r);l=1<<o,o=t[o],o>i&&(i=o),r&=~l}if(r=i,r=G()-r,r=(120>r?120:480>r?480:1080>r?1080:1920>r?1920:3e3>r?3e3:4320>r?4320:1960*fm(r/1960))-r,10<r){e.timeoutHandle=ro(Ot.bind(null,e,ge,et),r);break}Ot(e,ge,et);break;case 5:Ot(e,ge,et);break;default:throw Error(E(329))}}}return we(e,G()),e.callbackNode===n?md.bind(null,e):null}function No(e,t){var n=Xn;return e.current.memoizedState.isDehydrated&&(It(e,t).flags|=256),e=bi(e,t),e!==2&&(t=ge,ge=n,t!==null&&jo(t)),e}function jo(e){ge===null?ge=e:ge.push.apply(ge,e)}function pm(e){for(var t=e;;){if(t.flags&16384){var n=t.updateQueue;if(n!==null&&(n=n.stores,n!==null))for(var r=0;r<n.length;r++){var i=n[r],l=i.getSnapshot;i=i.value;try{if(!Ve(l(),i))return!1}catch{return!1}}}if(n=t.child,t.subtreeFlags&16384&&n!==null)n.return=t,t=n;else{if(t===e)break;for(;t.sibling===null;){if(t.return===null||t.return===e)return!0;t=t.return}t.sibling.return=t.return,t=t.sibling}}return!0}function ht(e,t){for(t&=~gs,t&=~Hi,e.suspendedLanes|=t,e.pingedLanes&=~t,e=e.expirationTimes;0<t;){var n=31-$e(t),r=1<<n;e[n]=-1,t&=~r}}function Ma(e){if(A&6)throw Error(E(327));gn();var t=fi(e,0);if(!(t&1))return we(e,G()),null;var n=bi(e,t);if(e.tag!==0&&n===2){var r=ql(e);r!==0&&(t=r,n=No(e,r))}if(n===1)throw n=hr,It(e,0),ht(e,t),we(e,G()),n;if(n===6)throw Error(E(345));return e.finishedWork=e.current.alternate,e.finishedLanes=t,Ot(e,ge,et),we(e,G()),null}function vs(e,t){var n=A;A|=1;try{return e(t)}finally{A=n,A===0&&(En=G()+500,Di&&bt())}}function Wt(e){yt!==null&&yt.tag===0&&!(A&6)&&gn();var t=A;A|=1;var n=Le.transition,r=F;try{if(Le.transition=null,F=1,e)return e()}finally{F=r,Le.transition=n,A=t,!(A&6)&&bt()}}function xs(){Ee=cn.current,$(cn)}function It(e,t){e.finishedWork=null,e.finishedLanes=0;var n=e.timeoutHandle;if(n!==-1&&(e.timeoutHandle=-1,Hp(n)),Y!==null)for(n=Y.return;n!==null;){var r=n;switch(Zo(r),r.tag){case 1:r=r.type.childContextTypes,r!=null&&yi();break;case 3:Sn(),$(ve),$(ue),as();break;case 5:ss(r);break;case 4:Sn();break;case 13:$(V);break;case 19:$(V);break;case 10:rs(r.type._context);break;case 22:case 23:xs()}n=n.return}if(ee=e,Y=e=jt(e.current,null),ne=Ee=t,J=0,hr=null,gs=Hi=Vt=0,ge=Xn=null,At!==null){for(t=0;t<At.length;t++)if(n=At[t],r=n.interleaved,r!==null){n.interleaved=null;var i=r.next,l=n.pending;if(l!==null){var o=l.next;l.next=i,r.next=o}n.pending=r}At=null}return e}function hd(e,t){do{var n=Y;try{if(ns(),Zr.current=Ci,ji){for(var r=W.memoizedState;r!==null;){var i=r.queue;i!==null&&(i.pending=null),r=r.next}ji=!1}if(Ht=0,Z=X=W=null,qn=!1,fr=0,hs.current=null,n===null||n.return===null){J=1,hr=t,Y=null;break}e:{var l=e,o=n.return,s=n,a=t;if(t=ne,s.flags|=32768,a!==null&&typeof a=="object"&&typeof a.then=="function"){var c=a,f=s,d=f.tag;if(!(f.mode&1)&&(d===0||d===11||d===15)){var h=f.alternate;h?(f.updateQueue=h.updateQueue,f.memoizedState=h.memoizedState,f.lanes=h.lanes):(f.updateQueue=null,f.memoizedState=null)}var w=Ea(o);if(w!==null){w.flags&=-257,Na(w,o,s,l,t),w.mode&1&&ka(l,c,t),t=w,a=c;var m=t.updateQueue;if(m===null){var v=new Set;v.add(a),t.updateQueue=v}else m.add(a);break e}else{if(!(t&1)){ka(l,c,t),ws();break e}a=Error(E(426))}}else if(H&&s.mode&1){var k=Ea(o);if(k!==null){!(k.flags&65536)&&(k.flags|=256),Na(k,o,s,l,t),es(kn(a,s));break e}}l=a=kn(a,s),J!==4&&(J=2),Xn===null?Xn=[l]:Xn.push(l),l=o;do{switch(l.tag){case 3:l.flags|=65536,t&=-t,l.lanes|=t;var g=Jc(l,a,t);ga(l,g);break e;case 1:s=a;var p=l.type,y=l.stateNode;if(!(l.flags&128)&&(typeof p.getDerivedStateFromError=="function"||y!==null&&typeof y.componentDidCatch=="function"&&(Et===null||!Et.has(y)))){l.flags|=65536,t&=-t,l.lanes|=t;var S=Zc(l,s,t);ga(l,S);break e}}l=l.return}while(l!==null)}vd(n)}catch(N){t=N,Y===n&&n!==null&&(Y=n=n.return);continue}break}while(!0)}function gd(){var e=_i.current;return _i.current=Ci,e===null?Ci:e}function ws(){(J===0||J===3||J===2)&&(J=4),ee===null||!(Vt&268435455)&&!(Hi&268435455)||ht(ee,ne)}function bi(e,t){var n=A;A|=2;var r=gd();(ee!==e||ne!==t)&&(et=null,It(e,t));do try{mm();break}catch(i){hd(e,i)}while(!0);if(ns(),A=n,_i.current=r,Y!==null)throw Error(E(261));return ee=null,ne=0,J}function mm(){for(;Y!==null;)yd(Y)}function hm(){for(;Y!==null&&!Uf();)yd(Y)}function yd(e){var t=wd(e.alternate,e,Ee);e.memoizedProps=e.pendingProps,t===null?vd(e):Y=t,hs.current=null}function vd(e){var t=e;do{var n=t.alternate;if(e=t.return,t.flags&32768){if(n=am(n,t),n!==null){n.flags&=32767,Y=n;return}if(e!==null)e.flags|=32768,e.subtreeFlags=0,e.deletions=null;else{J=6,Y=null;return}}else if(n=sm(n,t,Ee),n!==null){Y=n;return}if(t=t.sibling,t!==null){Y=t;return}Y=t=e}while(t!==null);J===0&&(J=5)}function Ot(e,t,n){var r=F,i=Le.transition;try{Le.transition=null,F=1,gm(e,t,n,r)}finally{Le.transition=i,F=r}return null}function gm(e,t,n,r){do gn();while(yt!==null);if(A&6)throw Error(E(327));n=e.finishedWork;var i=e.finishedLanes;if(n===null)return null;if(e.finishedWork=null,e.finishedLanes=0,n===e.current)throw Error(E(177));e.callbackNode=null,e.callbackPriority=0;var l=n.lanes|n.childLanes;if(Yf(e,l),e===ee&&(Y=ee=null,ne=0),!(n.subtreeFlags&2064)&&!(n.flags&2064)||Vr||(Vr=!0,Sd(di,function(){return gn(),null})),l=(n.flags&15990)!==0,n.subtreeFlags&15990||l){l=Le.transition,Le.transition=null;var o=F;F=1;var s=A;A|=4,hs.current=null,cm(e,n),fd(n,e),Mp(to),pi=!!eo,to=eo=null,e.current=n,dm(n),Bf(),A=s,F=o,Le.transition=l}else e.current=n;if(Vr&&(Vr=!1,yt=e,Ti=i),l=e.pendingLanes,l===0&&(Et=null),Vf(n.stateNode),we(e,G()),t!==null)for(r=e.onRecoverableError,n=0;n<t.length;n++)i=t[n],r(i.value,{componentStack:i.stack,digest:i.digest});if(Ri)throw Ri=!1,e=ko,ko=null,e;return Ti&1&&e.tag!==0&&gn(),l=e.pendingLanes,l&1?e===Eo?Jn++:(Jn=0,Eo=e):Jn=0,bt(),null}function gn(){if(yt!==null){var e=Ju(Ti),t=Le.transition,n=F;try{if(Le.transition=null,F=16>e?16:e,yt===null)var r=!1;else{if(e=yt,yt=null,Ti=0,A&6)throw Error(E(331));var i=A;for(A|=4,_=e.current;_!==null;){var l=_,o=l.child;if(_.flags&16){var s=l.deletions;if(s!==null){for(var a=0;a<s.length;a++){var c=s[a];for(_=c;_!==null;){var f=_;switch(f.tag){case 0:case 11:case 15:Yn(8,f,l)}var d=f.child;if(d!==null)d.return=f,_=d;else for(;_!==null;){f=_;var h=f.sibling,w=f.return;if(ud(f),f===c){_=null;break}if(h!==null){h.return=w,_=h;break}_=w}}}var m=l.alternate;if(m!==null){var v=m.child;if(v!==null){m.child=null;do{var k=v.sibling;v.sibling=null,v=k}while(v!==null)}}_=l}}if(l.subtreeFlags&2064&&o!==null)o.return=l,_=o;else e:for(;_!==null;){if(l=_,l.flags&2048)switch(l.tag){case 0:case 11:case 15:Yn(9,l,l.return)}var g=l.sibling;if(g!==null){g.return=l.return,_=g;break e}_=l.return}}var p=e.current;for(_=p;_!==null;){o=_;var y=o.child;if(o.subtreeFlags&2064&&y!==null)y.return=o,_=y;else e:for(o=p;_!==null;){if(s=_,s.flags&2048)try{switch(s.tag){case 0:case 11:case 15:$i(9,s)}}catch(N){Q(s,s.return,N)}if(s===o){_=null;break e}var S=s.sibling;if(S!==null){S.return=s.return,_=S;break e}_=s.return}}if(A=i,bt(),Je&&typeof Je.onPostCommitFiberRoot=="function")try{Je.onPostCommitFiberRoot(Li,e)}catch{}r=!0}return r}finally{F=n,Le.transition=t}}return!1}function Fa(e,t,n){t=kn(n,t),t=Jc(e,t,1),e=kt(e,t,1),t=de(),e!==null&&(vr(e,1,t),we(e,t))}function Q(e,t,n){if(e.tag===3)Fa(e,e,n);else for(;t!==null;){if(t.tag===3){Fa(t,e,n);break}else if(t.tag===1){var r=t.stateNode;if(typeof t.type.getDerivedStateFromError=="function"||typeof r.componentDidCatch=="function"&&(Et===null||!Et.has(r))){e=kn(n,e),e=Zc(t,e,1),t=kt(t,e,1),e=de(),t!==null&&(vr(t,1,e),we(t,e));break}}t=t.return}}function ym(e,t,n){var r=e.pingCache;r!==null&&r.delete(t),t=de(),e.pingedLanes|=e.suspendedLanes&n,ee===e&&(ne&n)===n&&(J===4||J===3&&(ne&130023424)===ne&&500>G()-ys?It(e,0):gs|=n),we(e,t)}function xd(e,t){t===0&&(e.mode&1?(t=Lr,Lr<<=1,!(Lr&130023424)&&(Lr=4194304)):t=1);var n=de();e=st(e,t),e!==null&&(vr(e,t,n),we(e,n))}function vm(e){var t=e.memoizedState,n=0;t!==null&&(n=t.retryLane),xd(e,n)}function xm(e,t){var n=0;switch(e.tag){case 13:var r=e.stateNode,i=e.memoizedState;i!==null&&(n=i.retryLane);break;case 19:r=e.stateNode;break;default:throw Error(E(314))}r!==null&&r.delete(t),xd(e,n)}var wd;wd=function(e,t,n){if(e!==null)if(e.memoizedProps!==t.pendingProps||ve.current)ye=!0;else{if(!(e.lanes&n)&&!(t.flags&128))return ye=!1,om(e,t,n);ye=!!(e.flags&131072)}else ye=!1,H&&t.flags&1048576&&Nc(t,wi,t.index);switch(t.lanes=0,t.tag){case 2:var r=t.type;ti(e,t),e=t.pendingProps;var i=vn(t,ue.current);hn(t,n),i=cs(null,t,r,e,i,n);var l=ds();return t.flags|=1,typeof i=="object"&&i!==null&&typeof i.render=="function"&&i.$$typeof===void 0?(t.tag=1,t.memoizedState=null,t.updateQueue=null,xe(r)?(l=!0,vi(t)):l=!1,t.memoizedState=i.state!==null&&i.state!==void 0?i.state:null,ls(t),i.updater=Bi,t.stateNode=i,i._reactInternals=t,co(t,r,e,n),t=mo(null,t,r,!0,l,n)):(t.tag=0,H&&l&&Jo(t),ce(null,t,i,n),t=t.child),t;case 16:r=t.elementType;e:{switch(ti(e,t),e=t.pendingProps,i=r._init,r=i(r._payload),t.type=r,i=t.tag=Sm(r),e=De(r,e),i){case 0:t=po(null,t,r,e,n);break e;case 1:t=_a(null,t,r,e,n);break e;case 11:t=ja(null,t,r,e,n);break e;case 14:t=Ca(null,t,r,De(r.type,e),n);break e}throw Error(E(306,r,""))}return t;case 0:return r=t.type,i=t.pendingProps,i=t.elementType===r?i:De(r,i),po(e,t,r,i,n);case 1:return r=t.type,i=t.pendingProps,i=t.elementType===r?i:De(r,i),_a(e,t,r,i,n);case 3:e:{if(rd(t),e===null)throw Error(E(387));r=t.pendingProps,l=t.memoizedState,i=l.element,bc(e,t),Ei(t,r,null,n);var o=t.memoizedState;if(r=o.element,l.isDehydrated)if(l={element:r,isDehydrated:!1,cache:o.cache,pendingSuspenseBoundaries:o.pendingSuspenseBoundaries,transitions:o.transitions},t.updateQueue.baseState=l,t.memoizedState=l,t.flags&256){i=kn(Error(E(423)),t),t=Ra(e,t,r,n,i);break e}else if(r!==i){i=kn(Error(E(424)),t),t=Ra(e,t,r,n,i);break e}else for(Ne=St(t.stateNode.containerInfo.firstChild),Ce=t,H=!0,Be=null,n=Rc(t,null,r,n),t.child=n;n;)n.flags=n.flags&-3|4096,n=n.sibling;else{if(xn(),r===i){t=at(e,t,n);break e}ce(e,t,r,n)}t=t.child}return t;case 5:return Pc(t),e===null&&so(t),r=t.type,i=t.pendingProps,l=e!==null?e.memoizedProps:null,o=i.children,no(r,i)?o=null:l!==null&&no(r,l)&&(t.flags|=32),nd(e,t),ce(e,t,o,n),t.child;case 6:return e===null&&so(t),null;case 13:return id(e,t,n);case 4:return os(t,t.stateNode.containerInfo),r=t.pendingProps,e===null?t.child=wn(t,null,r,n):ce(e,t,r,n),t.child;case 11:return r=t.type,i=t.pendingProps,i=t.elementType===r?i:De(r,i),ja(e,t,r,i,n);case 7:return ce(e,t,t.pendingProps,n),t.child;case 8:return ce(e,t,t.pendingProps.children,n),t.child;case 12:return ce(e,t,t.pendingProps.children,n),t.child;case 10:e:{if(r=t.type._context,i=t.pendingProps,l=t.memoizedProps,o=i.value,D(Si,r._currentValue),r._currentValue=o,l!==null)if(Ve(l.value,o)){if(l.children===i.children&&!ve.current){t=at(e,t,n);break e}}else for(l=t.child,l!==null&&(l.return=t);l!==null;){var s=l.dependencies;if(s!==null){o=l.child;for(var a=s.firstContext;a!==null;){if(a.context===r){if(l.tag===1){a=it(-1,n&-n),a.tag=2;var c=l.updateQueue;if(c!==null){c=c.shared;var f=c.pending;f===null?a.next=a:(a.next=f.next,f.next=a),c.pending=a}}l.lanes|=n,a=l.alternate,a!==null&&(a.lanes|=n),ao(l.return,n,t),s.lanes|=n;break}a=a.next}}else if(l.tag===10)o=l.type===t.type?null:l.child;else if(l.tag===18){if(o=l.return,o===null)throw Error(E(341));o.lanes|=n,s=o.alternate,s!==null&&(s.lanes|=n),ao(o,n,t),o=l.sibling}else o=l.child;if(o!==null)o.return=l;else for(o=l;o!==null;){if(o===t){o=null;break}if(l=o.sibling,l!==null){l.return=o.return,o=l;break}o=o.return}l=o}ce(e,t,i.children,n),t=t.child}return t;case 9:return i=t.type,r=t.pendingProps.children,hn(t,n),i=Ae(i),r=r(i),t.flags|=1,ce(e,t,r,n),t.child;case 14:return r=t.type,i=De(r,t.pendingProps),i=De(r.type,i),Ca(e,t,r,i,n);case 15:return ed(e,t,t.type,t.pendingProps,n);case 17:return r=t.type,i=t.pendingProps,i=t.elementType===r?i:De(r,i),ti(e,t),t.tag=1,xe(r)?(e=!0,vi(t)):e=!1,hn(t,n),Xc(t,r,i),co(t,r,i,n),mo(null,t,r,!0,e,n);case 19:return ld(e,t,n);case 22:return td(e,t,n)}throw Error(E(156,t.tag))};function Sd(e,t){return Gu(e,t)}function wm(e,t,n,r){this.tag=e,this.key=n,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.ref=null,this.pendingProps=t,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=r,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function Oe(e,t,n,r){return new wm(e,t,n,r)}function Ss(e){return e=e.prototype,!(!e||!e.isReactComponent)}function Sm(e){if(typeof e=="function")return Ss(e)?1:0;if(e!=null){if(e=e.$$typeof,e===Uo)return 11;if(e===Bo)return 14}return 2}function jt(e,t){var n=e.alternate;return n===null?(n=Oe(e.tag,t,e.key,e.mode),n.elementType=e.elementType,n.type=e.type,n.stateNode=e.stateNode,n.alternate=e,e.alternate=n):(n.pendingProps=t,n.type=e.type,n.flags=0,n.subtreeFlags=0,n.deletions=null),n.flags=e.flags&14680064,n.childLanes=e.childLanes,n.lanes=e.lanes,n.child=e.child,n.memoizedProps=e.memoizedProps,n.memoizedState=e.memoizedState,n.updateQueue=e.updateQueue,t=e.dependencies,n.dependencies=t===null?null:{lanes:t.lanes,firstContext:t.firstContext},n.sibling=e.sibling,n.index=e.index,n.ref=e.ref,n}function ii(e,t,n,r,i,l){var o=2;if(r=e,typeof e=="function")Ss(e)&&(o=1);else if(typeof e=="string")o=5;else e:switch(e){case Zt:return Dt(n.children,i,l,t);case Do:o=8,i|=8;break;case Ll:return e=Oe(12,n,t,i|2),e.elementType=Ll,e.lanes=l,e;case Al:return e=Oe(13,n,t,i),e.elementType=Al,e.lanes=l,e;case Ml:return e=Oe(19,n,t,i),e.elementType=Ml,e.lanes=l,e;case Pu:return Vi(n,i,l,t);default:if(typeof e=="object"&&e!==null)switch(e.$$typeof){case Tu:o=10;break e;case bu:o=9;break e;case Uo:o=11;break e;case Bo:o=14;break e;case ft:o=16,r=null;break e}throw Error(E(130,e==null?e:typeof e,""))}return t=Oe(o,n,t,i),t.elementType=e,t.type=r,t.lanes=l,t}function Dt(e,t,n,r){return e=Oe(7,e,r,t),e.lanes=n,e}function Vi(e,t,n,r){return e=Oe(22,e,r,t),e.elementType=Pu,e.lanes=n,e.stateNode={isHidden:!1},e}function Cl(e,t,n){return e=Oe(6,e,null,t),e.lanes=n,e}function _l(e,t,n){return t=Oe(4,e.children!==null?e.children:[],e.key,t),t.lanes=n,t.stateNode={containerInfo:e.containerInfo,pendingChildren:null,implementation:e.implementation},t}function km(e,t,n,r,i){this.tag=t,this.containerInfo=e,this.finishedWork=this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.pendingContext=this.context=null,this.callbackPriority=0,this.eventTimes=sl(0),this.expirationTimes=sl(-1),this.entangledLanes=this.finishedLanes=this.mutableReadLanes=this.expiredLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=sl(0),this.identifierPrefix=r,this.onRecoverableError=i,this.mutableSourceEagerHydrationData=null}function ks(e,t,n,r,i,l,o,s,a){return e=new km(e,t,n,s,a),t===1?(t=1,l===!0&&(t|=8)):t=0,l=Oe(3,null,null,t),e.current=l,l.stateNode=e,l.memoizedState={element:r,isDehydrated:n,cache:null,transitions:null,pendingSuspenseBoundaries:null},ls(l),e}function Em(e,t,n){var r=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:Jt,key:r==null?null:""+r,children:e,containerInfo:t,implementation:n}}function kd(e){if(!e)return _t;e=e._reactInternals;e:{if(Gt(e)!==e||e.tag!==1)throw Error(E(170));var t=e;do{switch(t.tag){case 3:t=t.stateNode.context;break e;case 1:if(xe(t.type)){t=t.stateNode.__reactInternalMemoizedMergedChildContext;break e}}t=t.return}while(t!==null);throw Error(E(171))}if(e.tag===1){var n=e.type;if(xe(n))return kc(e,n,t)}return t}function Ed(e,t,n,r,i,l,o,s,a){return e=ks(n,r,!0,e,i,l,o,s,a),e.context=kd(null),n=e.current,r=de(),i=Nt(n),l=it(r,i),l.callback=t??null,kt(n,l,i),e.current.lanes=i,vr(e,i,r),we(e,r),e}function Wi(e,t,n,r){var i=t.current,l=de(),o=Nt(i);return n=kd(n),t.context===null?t.context=n:t.pendingContext=n,t=it(l,o),t.payload={element:e},r=r===void 0?null:r,r!==null&&(t.callback=r),e=kt(i,t,o),e!==null&&(He(e,i,o,l),Jr(e,i,o)),o}function Pi(e){if(e=e.current,!e.child)return null;switch(e.child.tag){case 5:return e.child.stateNode;default:return e.child.stateNode}}function Ia(e,t){if(e=e.memoizedState,e!==null&&e.dehydrated!==null){var n=e.retryLane;e.retryLane=n!==0&&n<t?n:t}}function Es(e,t){Ia(e,t),(e=e.alternate)&&Ia(e,t)}function Nm(){return null}var Nd=typeof reportError=="function"?reportError:function(e){console.error(e)};function Ns(e){this._internalRoot=e}Ki.prototype.render=Ns.prototype.render=function(e){var t=this._internalRoot;if(t===null)throw Error(E(409));Wi(e,t,null,null)};Ki.prototype.unmount=Ns.prototype.unmount=function(){var e=this._internalRoot;if(e!==null){this._internalRoot=null;var t=e.containerInfo;Wt(function(){Wi(null,e,null,null)}),t[ot]=null}};function Ki(e){this._internalRoot=e}Ki.prototype.unstable_scheduleHydration=function(e){if(e){var t=tc();e={blockedOn:null,target:e,priority:t};for(var n=0;n<mt.length&&t!==0&&t<mt[n].priority;n++);mt.splice(n,0,e),n===0&&rc(e)}};function js(e){return!(!e||e.nodeType!==1&&e.nodeType!==9&&e.nodeType!==11)}function Qi(e){return!(!e||e.nodeType!==1&&e.nodeType!==9&&e.nodeType!==11&&(e.nodeType!==8||e.nodeValue!==" react-mount-point-unstable "))}function Da(){}function jm(e,t,n,r,i){if(i){if(typeof r=="function"){var l=r;r=function(){var c=Pi(o);l.call(c)}}var o=Ed(t,r,e,0,null,!1,!1,"",Da);return e._reactRootContainer=o,e[ot]=o.current,sr(e.nodeType===8?e.parentNode:e),Wt(),o}for(;i=e.lastChild;)e.removeChild(i);if(typeof r=="function"){var s=r;r=function(){var c=Pi(a);s.call(c)}}var a=ks(e,0,!1,null,null,!1,!1,"",Da);return e._reactRootContainer=a,e[ot]=a.current,sr(e.nodeType===8?e.parentNode:e),Wt(function(){Wi(t,a,n,r)}),a}function Gi(e,t,n,r,i){var l=n._reactRootContainer;if(l){var o=l;if(typeof i=="function"){var s=i;i=function(){var a=Pi(o);s.call(a)}}Wi(t,o,e,i)}else o=jm(n,t,e,i,r);return Pi(o)}Zu=function(e){switch(e.tag){case 3:var t=e.stateNode;if(t.current.memoizedState.isDehydrated){var n=$n(t.pendingLanes);n!==0&&(Vo(t,n|1),we(t,G()),!(A&6)&&(En=G()+500,bt()))}break;case 13:Wt(function(){var r=st(e,1);if(r!==null){var i=de();He(r,e,1,i)}}),Es(e,1)}};Wo=function(e){if(e.tag===13){var t=st(e,134217728);if(t!==null){var n=de();He(t,e,134217728,n)}Es(e,134217728)}};ec=function(e){if(e.tag===13){var t=Nt(e),n=st(e,t);if(n!==null){var r=de();He(n,e,t,r)}Es(e,t)}};tc=function(){return F};nc=function(e,t){var n=F;try{return F=e,t()}finally{F=n}};Kl=function(e,t,n){switch(t){case"input":if(Dl(e,n),t=n.name,n.type==="radio"&&t!=null){for(n=e;n.parentNode;)n=n.parentNode;for(n=n.querySelectorAll("input[name="+JSON.stringify(""+t)+'][type="radio"]'),t=0;t<n.length;t++){var r=n[t];if(r!==e&&r.form===e.form){var i=Ii(r);if(!i)throw Error(E(90));Ou(r),Dl(r,i)}}}break;case"textarea":Au(e,n);break;case"select":t=n.value,t!=null&&dn(e,!!n.multiple,t,!1)}};$u=vs;Hu=Wt;var Cm={usingClientEntryPoint:!1,Events:[wr,rn,Ii,Uu,Bu,vs]},In={findFiberByHostInstance:Lt,bundleType:0,version:"18.3.1",rendererPackageName:"react-dom"},_m={bundleType:In.bundleType,version:In.version,rendererPackageName:In.rendererPackageName,rendererConfig:In.rendererConfig,overrideHookState:null,overrideHookStateDeletePath:null,overrideHookStateRenamePath:null,overrideProps:null,overridePropsDeletePath:null,overridePropsRenamePath:null,setErrorHandler:null,setSuspenseHandler:null,scheduleUpdate:null,currentDispatcherRef:ut.ReactCurrentDispatcher,findHostInstanceByFiber:function(e){return e=Ku(e),e===null?null:e.stateNode},findFiberByHostInstance:In.findFiberByHostInstance||Nm,findHostInstancesForRefresh:null,scheduleRefresh:null,scheduleRoot:null,setRefreshHandler:null,getCurrentFiber:null,reconcilerVersion:"18.3.1-next-f1338f8080-20240426"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"){var Wr=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!Wr.isDisabled&&Wr.supportsFiber)try{Li=Wr.inject(_m),Je=Wr}catch{}}Re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED=Cm;Re.createPortal=function(e,t){var n=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!js(t))throw Error(E(200));return Em(e,t,null,n)};Re.createRoot=function(e,t){if(!js(e))throw Error(E(299));var n=!1,r="",i=Nd;return t!=null&&(t.unstable_strictMode===!0&&(n=!0),t.identifierPrefix!==void 0&&(r=t.identifierPrefix),t.onRecoverableError!==void 0&&(i=t.onRecoverableError)),t=ks(e,1,!1,null,null,n,!1,r,i),e[ot]=t.current,sr(e.nodeType===8?e.parentNode:e),new Ns(t)};Re.findDOMNode=function(e){if(e==null)return null;if(e.nodeType===1)return e;var t=e._reactInternals;if(t===void 0)throw typeof e.render=="function"?Error(E(188)):(e=Object.keys(e).join(","),Error(E(268,e)));return e=Ku(t),e=e===null?null:e.stateNode,e};Re.flushSync=function(e){return Wt(e)};Re.hydrate=function(e,t,n){if(!Qi(t))throw Error(E(200));return Gi(null,e,t,!0,n)};Re.hydrateRoot=function(e,t,n){if(!js(e))throw Error(E(405));var r=n!=null&&n.hydratedSources||null,i=!1,l="",o=Nd;if(n!=null&&(n.unstable_strictMode===!0&&(i=!0),n.identifierPrefix!==void 0&&(l=n.identifierPrefix),n.onRecoverableError!==void 0&&(o=n.onRecoverableError)),t=Ed(t,null,e,1,n??null,i,!1,l,o),e[ot]=t.current,sr(e),r)for(e=0;e<r.length;e++)n=r[e],i=n._getVersion,i=i(n._source),t.mutableSourceEagerHydrationData==null?t.mutableSourceEagerHydrationData=[n,i]:t.mutableSourceEagerHydrationData.push(n,i);return new Ki(t)};Re.render=function(e,t,n){if(!Qi(t))throw Error(E(200));return Gi(null,e,t,!1,n)};Re.unmountComponentAtNode=function(e){if(!Qi(e))throw Error(E(40));return e._reactRootContainer?(Wt(function(){Gi(null,null,e,!1,function(){e._reactRootContainer=null,e[ot]=null})}),!0):!1};Re.unstable_batchedUpdates=vs;Re.unstable_renderSubtreeIntoContainer=function(e,t,n,r){if(!Qi(n))throw Error(E(200));if(e==null||e._reactInternals===void 0)throw Error(E(38));return Gi(e,t,n,!1,r)};Re.version="18.3.1-next-f1338f8080-20240426";function jd(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(jd)}catch(e){console.error(e)}}jd(),ju.exports=Re;var Rm=ju.exports,Ua=Rm;zl.createRoot=Ua.createRoot,zl.hydrateRoot=Ua.hydrateRoot;function Cd(e,t){return function(){return e.apply(t,arguments)}}const{toString:Tm}=Object.prototype,{getPrototypeOf:Cs}=Object,{iterator:qi,toStringTag:_d}=Symbol,Yi=(e=>t=>{const n=Tm.call(t);return e[n]||(e[n]=n.slice(8,-1).toLowerCase())})(Object.create(null)),We=e=>(e=e.toLowerCase(),t=>Yi(t)===e),Xi=e=>t=>typeof t===e,{isArray:bn}=Array,Nn=Xi("undefined");function kr(e){return e!==null&&!Nn(e)&&e.constructor!==null&&!Nn(e.constructor)&&Se(e.constructor.isBuffer)&&e.constructor.isBuffer(e)}const Rd=We("ArrayBuffer");function bm(e){let t;return typeof ArrayBuffer<"u"&&ArrayBuffer.isView?t=ArrayBuffer.isView(e):t=e&&e.buffer&&Rd(e.buffer),t}const Pm=Xi("string"),Se=Xi("function"),Td=Xi("number"),Er=e=>e!==null&&typeof e=="object",zm=e=>e===!0||e===!1,li=e=>{if(Yi(e)!=="object")return!1;const t=Cs(e);return(t===null||t===Object.prototype||Object.getPrototypeOf(t)===null)&&!(_d in e)&&!(qi in e)},Om=e=>{if(!Er(e)||kr(e))return!1;try{return Object.keys(e).length===0&&Object.getPrototypeOf(e)===Object.prototype}catch{return!1}},Lm=We("Date"),Am=We("File"),Mm=We("Blob"),Fm=We("FileList"),Im=e=>Er(e)&&Se(e.pipe),Dm=e=>{let t;return e&&(typeof FormData=="function"&&e instanceof FormData||Se(e.append)&&((t=Yi(e))==="formdata"||t==="object"&&Se(e.toString)&&e.toString()==="[object FormData]"))},Um=We("URLSearchParams"),[Bm,$m,Hm,Vm]=["ReadableStream","Request","Response","Headers"].map(We),Wm=e=>e.trim?e.trim():e.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,"");function Nr(e,t,{allOwnKeys:n=!1}={}){if(e===null||typeof e>"u")return;let r,i;if(typeof e!="object"&&(e=[e]),bn(e))for(r=0,i=e.length;r<i;r++)t.call(null,e[r],r,e);else{if(kr(e))return;const l=n?Object.getOwnPropertyNames(e):Object.keys(e),o=l.length;let s;for(r=0;r<o;r++)s=l[r],t.call(null,e[s],s,e)}}function bd(e,t){if(kr(e))return null;t=t.toLowerCase();const n=Object.keys(e);let r=n.length,i;for(;r-- >0;)if(i=n[r],t===i.toLowerCase())return i;return null}const Ft=typeof globalThis<"u"?globalThis:typeof self<"u"?self:typeof window<"u"?window:global,Pd=e=>!Nn(e)&&e!==Ft;function Co(){const{caseless:e,skipUndefined:t}=Pd(this)&&this||{},n={},r=(i,l)=>{const o=e&&bd(n,l)||l;li(n[o])&&li(i)?n[o]=Co(n[o],i):li(i)?n[o]=Co({},i):bn(i)?n[o]=i.slice():(!t||!Nn(i))&&(n[o]=i)};for(let i=0,l=arguments.length;i<l;i++)arguments[i]&&Nr(arguments[i],r);return n}const Km=(e,t,n,{allOwnKeys:r}={})=>(Nr(t,(i,l)=>{n&&Se(i)?Object.defineProperty(e,l,{value:Cd(i,n),writable:!0,enumerable:!0,configurable:!0}):Object.defineProperty(e,l,{value:i,writable:!0,enumerable:!0,configurable:!0})},{allOwnKeys:r}),e),Qm=e=>(e.charCodeAt(0)===65279&&(e=e.slice(1)),e),Gm=(e,t,n,r)=>{e.prototype=Object.create(t.prototype,r),Object.defineProperty(e.prototype,"constructor",{value:e,writable:!0,enumerable:!1,configurable:!0}),Object.defineProperty(e,"super",{value:t.prototype}),n&&Object.assign(e.prototype,n)},qm=(e,t,n,r)=>{let i,l,o;const s={};if(t=t||{},e==null)return t;do{for(i=Object.getOwnPropertyNames(e),l=i.length;l-- >0;)o=i[l],(!r||r(o,e,t))&&!s[o]&&(t[o]=e[o],s[o]=!0);e=n!==!1&&Cs(e)}while(e&&(!n||n(e,t))&&e!==Object.prototype);return t},Ym=(e,t,n)=>{e=String(e),(n===void 0||n>e.length)&&(n=e.length),n-=t.length;const r=e.indexOf(t,n);return r!==-1&&r===n},Xm=e=>{if(!e)return null;if(bn(e))return e;let t=e.length;if(!Td(t))return null;const n=new Array(t);for(;t-- >0;)n[t]=e[t];return n},Jm=(e=>t=>e&&t instanceof e)(typeof Uint8Array<"u"&&Cs(Uint8Array)),Zm=(e,t)=>{const r=(e&&e[qi]).call(e);let i;for(;(i=r.next())&&!i.done;){const l=i.value;t.call(e,l[0],l[1])}},eh=(e,t)=>{let n;const r=[];for(;(n=e.exec(t))!==null;)r.push(n);return r},th=We("HTMLFormElement"),nh=e=>e.toLowerCase().replace(/[-_\s]([a-z\d])(\w*)/g,function(n,r,i){return r.toUpperCase()+i}),Ba=(({hasOwnProperty:e})=>(t,n)=>e.call(t,n))(Object.prototype),rh=We("RegExp"),zd=(e,t)=>{const n=Object.getOwnPropertyDescriptors(e),r={};Nr(n,(i,l)=>{let o;(o=t(i,l,e))!==!1&&(r[l]=o||i)}),Object.defineProperties(e,r)},ih=e=>{zd(e,(t,n)=>{if(Se(e)&&["arguments","caller","callee"].indexOf(n)!==-1)return!1;const r=e[n];if(Se(r)){if(t.enumerable=!1,"writable"in t){t.writable=!1;return}t.set||(t.set=()=>{throw Error("Can not rewrite read-only method '"+n+"'")})}})},lh=(e,t)=>{const n={},r=i=>{i.forEach(l=>{n[l]=!0})};return bn(e)?r(e):r(String(e).split(t)),n},oh=()=>{},sh=(e,t)=>e!=null&&Number.isFinite(e=+e)?e:t;function ah(e){return!!(e&&Se(e.append)&&e[_d]==="FormData"&&e[qi])}const uh=e=>{const t=new Array(10),n=(r,i)=>{if(Er(r)){if(t.indexOf(r)>=0)return;if(kr(r))return r;if(!("toJSON"in r)){t[i]=r;const l=bn(r)?[]:{};return Nr(r,(o,s)=>{const a=n(o,i+1);!Nn(a)&&(l[s]=a)}),t[i]=void 0,l}}return r};return n(e,0)},ch=We("AsyncFunction"),dh=e=>e&&(Er(e)||Se(e))&&Se(e.then)&&Se(e.catch),Od=((e,t)=>e?setImmediate:t?((n,r)=>(Ft.addEventListener("message",({source:i,data:l})=>{i===Ft&&l===n&&r.length&&r.shift()()},!1),i=>{r.push(i),Ft.postMessage(n,"*")}))(`axios@${Math.random()}`,[]):n=>setTimeout(n))(typeof setImmediate=="function",Se(Ft.postMessage)),fh=typeof queueMicrotask<"u"?queueMicrotask.bind(Ft):typeof process<"u"&&process.nextTick||Od,ph=e=>e!=null&&Se(e[qi]),x={isArray:bn,isArrayBuffer:Rd,isBuffer:kr,isFormData:Dm,isArrayBufferView:bm,isString:Pm,isNumber:Td,isBoolean:zm,isObject:Er,isPlainObject:li,isEmptyObject:Om,isReadableStream:Bm,isRequest:$m,isResponse:Hm,isHeaders:Vm,isUndefined:Nn,isDate:Lm,isFile:Am,isBlob:Mm,isRegExp:rh,isFunction:Se,isStream:Im,isURLSearchParams:Um,isTypedArray:Jm,isFileList:Fm,forEach:Nr,merge:Co,extend:Km,trim:Wm,stripBOM:Qm,inherits:Gm,toFlatObject:qm,kindOf:Yi,kindOfTest:We,endsWith:Ym,toArray:Xm,forEachEntry:Zm,matchAll:eh,isHTMLForm:th,hasOwnProperty:Ba,hasOwnProp:Ba,reduceDescriptors:zd,freezeMethods:ih,toObjectSet:lh,toCamelCase:nh,noop:oh,toFiniteNumber:sh,findKey:bd,global:Ft,isContextDefined:Pd,isSpecCompliantForm:ah,toJSONObject:uh,isAsyncFn:ch,isThenable:dh,setImmediate:Od,asap:fh,isIterable:ph};let b=class Ld extends Error{static from(t,n,r,i,l,o){const s=new Ld(t.message,n||t.code,r,i,l);return s.cause=t,s.name=t.name,o&&Object.assign(s,o),s}constructor(t,n,r,i,l){super(t),this.name="AxiosError",this.isAxiosError=!0,n&&(this.code=n),r&&(this.config=r),i&&(this.request=i),l&&(this.response=l,this.status=l.status)}toJSON(){return{message:this.message,name:this.name,description:this.description,number:this.number,fileName:this.fileName,lineNumber:this.lineNumber,columnNumber:this.columnNumber,stack:this.stack,config:x.toJSONObject(this.config),code:this.code,status:this.status}}};b.ERR_BAD_OPTION_VALUE="ERR_BAD_OPTION_VALUE";b.ERR_BAD_OPTION="ERR_BAD_OPTION";b.ECONNABORTED="ECONNABORTED";b.ETIMEDOUT="ETIMEDOUT";b.ERR_NETWORK="ERR_NETWORK";b.ERR_FR_TOO_MANY_REDIRECTS="ERR_FR_TOO_MANY_REDIRECTS";b.ERR_DEPRECATED="ERR_DEPRECATED";b.ERR_BAD_RESPONSE="ERR_BAD_RESPONSE";b.ERR_BAD_REQUEST="ERR_BAD_REQUEST";b.ERR_CANCELED="ERR_CANCELED";b.ERR_NOT_SUPPORT="ERR_NOT_SUPPORT";b.ERR_INVALID_URL="ERR_INVALID_URL";const mh=null;function _o(e){return x.isPlainObject(e)||x.isArray(e)}function Ad(e){return x.endsWith(e,"[]")?e.slice(0,-2):e}function $a(e,t,n){return e?e.concat(t).map(function(i,l){return i=Ad(i),!n&&l?"["+i+"]":i}).join(n?".":""):t}function hh(e){return x.isArray(e)&&!e.some(_o)}const gh=x.toFlatObject(x,{},null,function(t){return/^is[A-Z]/.test(t)});function Ji(e,t,n){if(!x.isObject(e))throw new TypeError("target must be an object");t=t||new FormData,n=x.toFlatObject(n,{metaTokens:!0,dots:!1,indexes:!1},!1,function(v,k){return!x.isUndefined(k[v])});const r=n.metaTokens,i=n.visitor||f,l=n.dots,o=n.indexes,a=(n.Blob||typeof Blob<"u"&&Blob)&&x.isSpecCompliantForm(t);if(!x.isFunction(i))throw new TypeError("visitor must be a function");function c(m){if(m===null)return"";if(x.isDate(m))return m.toISOString();if(x.isBoolean(m))return m.toString();if(!a&&x.isBlob(m))throw new b("Blob is not supported. Use a Buffer instead.");return x.isArrayBuffer(m)||x.isTypedArray(m)?a&&typeof Blob=="function"?new Blob([m]):Buffer.from(m):m}function f(m,v,k){let g=m;if(m&&!k&&typeof m=="object"){if(x.endsWith(v,"{}"))v=r?v:v.slice(0,-2),m=JSON.stringify(m);else if(x.isArray(m)&&hh(m)||(x.isFileList(m)||x.endsWith(v,"[]"))&&(g=x.toArray(m)))return v=Ad(v),g.forEach(function(y,S){!(x.isUndefined(y)||y===null)&&t.append(o===!0?$a([v],S,l):o===null?v:v+"[]",c(y))}),!1}return _o(m)?!0:(t.append($a(k,v,l),c(m)),!1)}const d=[],h=Object.assign(gh,{defaultVisitor:f,convertValue:c,isVisitable:_o});function w(m,v){if(!x.isUndefined(m)){if(d.indexOf(m)!==-1)throw Error("Circular reference detected in "+v.join("."));d.push(m),x.forEach(m,function(g,p){(!(x.isUndefined(g)||g===null)&&i.call(t,g,x.isString(p)?p.trim():p,v,h))===!0&&w(g,v?v.concat(p):[p])}),d.pop()}}if(!x.isObject(e))throw new TypeError("data must be an object");return w(e),t}function Ha(e){const t={"!":"%21","'":"%27","(":"%28",")":"%29","~":"%7E","%20":"+","%00":"\0"};return encodeURIComponent(e).replace(/[!'()~]|%20|%00/g,function(r){return t[r]})}function _s(e,t){this._pairs=[],e&&Ji(e,this,t)}const Md=_s.prototype;Md.append=function(t,n){this._pairs.push([t,n])};Md.toString=function(t){const n=t?function(r){return t.call(this,r,Ha)}:Ha;return this._pairs.map(function(i){return n(i[0])+"="+n(i[1])},"").join("&")};function yh(e){return encodeURIComponent(e).replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%20/g,"+")}function Fd(e,t,n){if(!t)return e;const r=n&&n.encode||yh,i=x.isFunction(n)?{serialize:n}:n,l=i&&i.serialize;let o;if(l?o=l(t,i):o=x.isURLSearchParams(t)?t.toString():new _s(t,i).toString(r),o){const s=e.indexOf("#");s!==-1&&(e=e.slice(0,s)),e+=(e.indexOf("?")===-1?"?":"&")+o}return e}class Va{constructor(){this.handlers=[]}use(t,n,r){return this.handlers.push({fulfilled:t,rejected:n,synchronous:r?r.synchronous:!1,runWhen:r?r.runWhen:null}),this.handlers.length-1}eject(t){this.handlers[t]&&(this.handlers[t]=null)}clear(){this.handlers&&(this.handlers=[])}forEach(t){x.forEach(this.handlers,function(r){r!==null&&t(r)})}}const Id={silentJSONParsing:!0,forcedJSONParsing:!0,clarifyTimeoutError:!1},vh=typeof URLSearchParams<"u"?URLSearchParams:_s,xh=typeof FormData<"u"?FormData:null,wh=typeof Blob<"u"?Blob:null,Sh={isBrowser:!0,classes:{URLSearchParams:vh,FormData:xh,Blob:wh},protocols:["http","https","file","blob","url","data"]},Rs=typeof window<"u"&&typeof document<"u",Ro=typeof navigator=="object"&&navigator||void 0,kh=Rs&&(!Ro||["ReactNative","NativeScript","NS"].indexOf(Ro.product)<0),Eh=typeof WorkerGlobalScope<"u"&&self instanceof WorkerGlobalScope&&typeof self.importScripts=="function",Nh=Rs&&window.location.href||"http://localhost",jh=Object.freeze(Object.defineProperty({__proto__:null,hasBrowserEnv:Rs,hasStandardBrowserEnv:kh,hasStandardBrowserWebWorkerEnv:Eh,navigator:Ro,origin:Nh},Symbol.toStringTag,{value:"Module"})),se={...jh,...Sh};function Ch(e,t){return Ji(e,new se.classes.URLSearchParams,{visitor:function(n,r,i,l){return se.isNode&&x.isBuffer(n)?(this.append(r,n.toString("base64")),!1):l.defaultVisitor.apply(this,arguments)},...t})}function _h(e){return x.matchAll(/\w+|\[(\w*)]/g,e).map(t=>t[0]==="[]"?"":t[1]||t[0])}function Rh(e){const t={},n=Object.keys(e);let r;const i=n.length;let l;for(r=0;r<i;r++)l=n[r],t[l]=e[l];return t}function Dd(e){function t(n,r,i,l){let o=n[l++];if(o==="__proto__")return!0;const s=Number.isFinite(+o),a=l>=n.length;return o=!o&&x.isArray(i)?i.length:o,a?(x.hasOwnProp(i,o)?i[o]=[i[o],r]:i[o]=r,!s):((!i[o]||!x.isObject(i[o]))&&(i[o]=[]),t(n,r,i[o],l)&&x.isArray(i[o])&&(i[o]=Rh(i[o])),!s)}if(x.isFormData(e)&&x.isFunction(e.entries)){const n={};return x.forEachEntry(e,(r,i)=>{t(_h(r),i,n,0)}),n}return null}function Th(e,t,n){if(x.isString(e))try{return(t||JSON.parse)(e),x.trim(e)}catch(r){if(r.name!=="SyntaxError")throw r}return(n||JSON.stringify)(e)}const jr={transitional:Id,adapter:["xhr","http","fetch"],transformRequest:[function(t,n){const r=n.getContentType()||"",i=r.indexOf("application/json")>-1,l=x.isObject(t);if(l&&x.isHTMLForm(t)&&(t=new FormData(t)),x.isFormData(t))return i?JSON.stringify(Dd(t)):t;if(x.isArrayBuffer(t)||x.isBuffer(t)||x.isStream(t)||x.isFile(t)||x.isBlob(t)||x.isReadableStream(t))return t;if(x.isArrayBufferView(t))return t.buffer;if(x.isURLSearchParams(t))return n.setContentType("application/x-www-form-urlencoded;charset=utf-8",!1),t.toString();let s;if(l){if(r.indexOf("application/x-www-form-urlencoded")>-1)return Ch(t,this.formSerializer).toString();if((s=x.isFileList(t))||r.indexOf("multipart/form-data")>-1){const a=this.env&&this.env.FormData;return Ji(s?{"files[]":t}:t,a&&new a,this.formSerializer)}}return l||i?(n.setContentType("application/json",!1),Th(t)):t}],transformResponse:[function(t){const n=this.transitional||jr.transitional,r=n&&n.forcedJSONParsing,i=this.responseType==="json";if(x.isResponse(t)||x.isReadableStream(t))return t;if(t&&x.isString(t)&&(r&&!this.responseType||i)){const o=!(n&&n.silentJSONParsing)&&i;try{return JSON.parse(t,this.parseReviver)}catch(s){if(o)throw s.name==="SyntaxError"?b.from(s,b.ERR_BAD_RESPONSE,this,null,this.response):s}}return t}],timeout:0,xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN",maxContentLength:-1,maxBodyLength:-1,env:{FormData:se.classes.FormData,Blob:se.classes.Blob},validateStatus:function(t){return t>=200&&t<300},headers:{common:{Accept:"application/json, text/plain, */*","Content-Type":void 0}}};x.forEach(["delete","get","head","post","put","patch"],e=>{jr.headers[e]={}});const bh=x.toObjectSet(["age","authorization","content-length","content-type","etag","expires","from","host","if-modified-since","if-unmodified-since","last-modified","location","max-forwards","proxy-authorization","referer","retry-after","user-agent"]),Ph=e=>{const t={};let n,r,i;return e&&e.split(`
`).forEach(function(o){i=o.indexOf(":"),n=o.substring(0,i).trim().toLowerCase(),r=o.substring(i+1).trim(),!(!n||t[n]&&bh[n])&&(n==="set-cookie"?t[n]?t[n].push(r):t[n]=[r]:t[n]=t[n]?t[n]+", "+r:r)}),t},Wa=Symbol("internals");function Dn(e){return e&&String(e).trim().toLowerCase()}function oi(e){return e===!1||e==null?e:x.isArray(e)?e.map(oi):String(e)}function zh(e){const t=Object.create(null),n=/([^\s,;=]+)\s*(?:=\s*([^,;]+))?/g;let r;for(;r=n.exec(e);)t[r[1]]=r[2];return t}const Oh=e=>/^[-_a-zA-Z0-9^`|~,!#$%&'*+.]+$/.test(e.trim());function Rl(e,t,n,r,i){if(x.isFunction(r))return r.call(this,t,n);if(i&&(t=n),!!x.isString(t)){if(x.isString(r))return t.indexOf(r)!==-1;if(x.isRegExp(r))return r.test(t)}}function Lh(e){return e.trim().toLowerCase().replace(/([a-z\d])(\w*)/g,(t,n,r)=>n.toUpperCase()+r)}function Ah(e,t){const n=x.toCamelCase(" "+t);["get","set","has"].forEach(r=>{Object.defineProperty(e,r+n,{value:function(i,l,o){return this[r].call(this,t,i,l,o)},configurable:!0})})}let ke=class{constructor(t){t&&this.set(t)}set(t,n,r){const i=this;function l(s,a,c){const f=Dn(a);if(!f)throw new Error("header name must be a non-empty string");const d=x.findKey(i,f);(!d||i[d]===void 0||c===!0||c===void 0&&i[d]!==!1)&&(i[d||a]=oi(s))}const o=(s,a)=>x.forEach(s,(c,f)=>l(c,f,a));if(x.isPlainObject(t)||t instanceof this.constructor)o(t,n);else if(x.isString(t)&&(t=t.trim())&&!Oh(t))o(Ph(t),n);else if(x.isObject(t)&&x.isIterable(t)){let s={},a,c;for(const f of t){if(!x.isArray(f))throw TypeError("Object iterator must return a key-value pair");s[c=f[0]]=(a=s[c])?x.isArray(a)?[...a,f[1]]:[a,f[1]]:f[1]}o(s,n)}else t!=null&&l(n,t,r);return this}get(t,n){if(t=Dn(t),t){const r=x.findKey(this,t);if(r){const i=this[r];if(!n)return i;if(n===!0)return zh(i);if(x.isFunction(n))return n.call(this,i,r);if(x.isRegExp(n))return n.exec(i);throw new TypeError("parser must be boolean|regexp|function")}}}has(t,n){if(t=Dn(t),t){const r=x.findKey(this,t);return!!(r&&this[r]!==void 0&&(!n||Rl(this,this[r],r,n)))}return!1}delete(t,n){const r=this;let i=!1;function l(o){if(o=Dn(o),o){const s=x.findKey(r,o);s&&(!n||Rl(r,r[s],s,n))&&(delete r[s],i=!0)}}return x.isArray(t)?t.forEach(l):l(t),i}clear(t){const n=Object.keys(this);let r=n.length,i=!1;for(;r--;){const l=n[r];(!t||Rl(this,this[l],l,t,!0))&&(delete this[l],i=!0)}return i}normalize(t){const n=this,r={};return x.forEach(this,(i,l)=>{const o=x.findKey(r,l);if(o){n[o]=oi(i),delete n[l];return}const s=t?Lh(l):String(l).trim();s!==l&&delete n[l],n[s]=oi(i),r[s]=!0}),this}concat(...t){return this.constructor.concat(this,...t)}toJSON(t){const n=Object.create(null);return x.forEach(this,(r,i)=>{r!=null&&r!==!1&&(n[i]=t&&x.isArray(r)?r.join(", "):r)}),n}[Symbol.iterator](){return Object.entries(this.toJSON())[Symbol.iterator]()}toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join(`
`)}getSetCookie(){return this.get("set-cookie")||[]}get[Symbol.toStringTag](){return"AxiosHeaders"}static from(t){return t instanceof this?t:new this(t)}static concat(t,...n){const r=new this(t);return n.forEach(i=>r.set(i)),r}static accessor(t){const r=(this[Wa]=this[Wa]={accessors:{}}).accessors,i=this.prototype;function l(o){const s=Dn(o);r[s]||(Ah(i,o),r[s]=!0)}return x.isArray(t)?t.forEach(l):l(t),this}};ke.accessor(["Content-Type","Content-Length","Accept","Accept-Encoding","User-Agent","Authorization"]);x.reduceDescriptors(ke.prototype,({value:e},t)=>{let n=t[0].toUpperCase()+t.slice(1);return{get:()=>e,set(r){this[n]=r}}});x.freezeMethods(ke);function Tl(e,t){const n=this||jr,r=t||n,i=ke.from(r.headers);let l=r.data;return x.forEach(e,function(s){l=s.call(n,l,i.normalize(),t?t.status:void 0)}),i.normalize(),l}function Ud(e){return!!(e&&e.__CANCEL__)}let Cr=class extends b{constructor(t,n,r){super(t??"canceled",b.ERR_CANCELED,n,r),this.name="CanceledError",this.__CANCEL__=!0}};function Bd(e,t,n){const r=n.config.validateStatus;!n.status||!r||r(n.status)?e(n):t(new b("Request failed with status code "+n.status,[b.ERR_BAD_REQUEST,b.ERR_BAD_RESPONSE][Math.floor(n.status/100)-4],n.config,n.request,n))}function Mh(e){const t=/^([-+\w]{1,25})(:?\/\/|:)/.exec(e);return t&&t[1]||""}function Fh(e,t){e=e||10;const n=new Array(e),r=new Array(e);let i=0,l=0,o;return t=t!==void 0?t:1e3,function(a){const c=Date.now(),f=r[l];o||(o=c),n[i]=a,r[i]=c;let d=l,h=0;for(;d!==i;)h+=n[d++],d=d%e;if(i=(i+1)%e,i===l&&(l=(l+1)%e),c-o<t)return;const w=f&&c-f;return w?Math.round(h*1e3/w):void 0}}function Ih(e,t){let n=0,r=1e3/t,i,l;const o=(c,f=Date.now())=>{n=f,i=null,l&&(clearTimeout(l),l=null),e(...c)};return[(...c)=>{const f=Date.now(),d=f-n;d>=r?o(c,f):(i=c,l||(l=setTimeout(()=>{l=null,o(i)},r-d)))},()=>i&&o(i)]}const zi=(e,t,n=3)=>{let r=0;const i=Fh(50,250);return Ih(l=>{const o=l.loaded,s=l.lengthComputable?l.total:void 0,a=o-r,c=i(a),f=o<=s;r=o;const d={loaded:o,total:s,progress:s?o/s:void 0,bytes:a,rate:c||void 0,estimated:c&&s&&f?(s-o)/c:void 0,event:l,lengthComputable:s!=null,[t?"download":"upload"]:!0};e(d)},n)},Ka=(e,t)=>{const n=e!=null;return[r=>t[0]({lengthComputable:n,total:e,loaded:r}),t[1]]},Qa=e=>(...t)=>x.asap(()=>e(...t)),Dh=se.hasStandardBrowserEnv?((e,t)=>n=>(n=new URL(n,se.origin),e.protocol===n.protocol&&e.host===n.host&&(t||e.port===n.port)))(new URL(se.origin),se.navigator&&/(msie|trident)/i.test(se.navigator.userAgent)):()=>!0,Uh=se.hasStandardBrowserEnv?{write(e,t,n,r,i,l,o){if(typeof document>"u")return;const s=[`${e}=${encodeURIComponent(t)}`];x.isNumber(n)&&s.push(`expires=${new Date(n).toUTCString()}`),x.isString(r)&&s.push(`path=${r}`),x.isString(i)&&s.push(`domain=${i}`),l===!0&&s.push("secure"),x.isString(o)&&s.push(`SameSite=${o}`),document.cookie=s.join("; ")},read(e){if(typeof document>"u")return null;const t=document.cookie.match(new RegExp("(?:^|; )"+e+"=([^;]*)"));return t?decodeURIComponent(t[1]):null},remove(e){this.write(e,"",Date.now()-864e5,"/")}}:{write(){},read(){return null},remove(){}};function Bh(e){return/^([a-z][a-z\d+\-.]*:)?\/\//i.test(e)}function $h(e,t){return t?e.replace(/\/?\/$/,"")+"/"+t.replace(/^\/+/,""):e}function $d(e,t,n){let r=!Bh(t);return e&&(r||n==!1)?$h(e,t):t}const Ga=e=>e instanceof ke?{...e}:e;function Kt(e,t){t=t||{};const n={};function r(c,f,d,h){return x.isPlainObject(c)&&x.isPlainObject(f)?x.merge.call({caseless:h},c,f):x.isPlainObject(f)?x.merge({},f):x.isArray(f)?f.slice():f}function i(c,f,d,h){if(x.isUndefined(f)){if(!x.isUndefined(c))return r(void 0,c,d,h)}else return r(c,f,d,h)}function l(c,f){if(!x.isUndefined(f))return r(void 0,f)}function o(c,f){if(x.isUndefined(f)){if(!x.isUndefined(c))return r(void 0,c)}else return r(void 0,f)}function s(c,f,d){if(d in t)return r(c,f);if(d in e)return r(void 0,c)}const a={url:l,method:l,data:l,baseURL:o,transformRequest:o,transformResponse:o,paramsSerializer:o,timeout:o,timeoutMessage:o,withCredentials:o,withXSRFToken:o,adapter:o,responseType:o,xsrfCookieName:o,xsrfHeaderName:o,onUploadProgress:o,onDownloadProgress:o,decompress:o,maxContentLength:o,maxBodyLength:o,beforeRedirect:o,transport:o,httpAgent:o,httpsAgent:o,cancelToken:o,socketPath:o,responseEncoding:o,validateStatus:s,headers:(c,f,d)=>i(Ga(c),Ga(f),d,!0)};return x.forEach(Object.keys({...e,...t}),function(f){const d=a[f]||i,h=d(e[f],t[f],f);x.isUndefined(h)&&d!==s||(n[f]=h)}),n}const Hd=e=>{const t=Kt({},e);let{data:n,withXSRFToken:r,xsrfHeaderName:i,xsrfCookieName:l,headers:o,auth:s}=t;if(t.headers=o=ke.from(o),t.url=Fd($d(t.baseURL,t.url,t.allowAbsoluteUrls),e.params,e.paramsSerializer),s&&o.set("Authorization","Basic "+btoa((s.username||"")+":"+(s.password?unescape(encodeURIComponent(s.password)):""))),x.isFormData(n)){if(se.hasStandardBrowserEnv||se.hasStandardBrowserWebWorkerEnv)o.setContentType(void 0);else if(x.isFunction(n.getHeaders)){const a=n.getHeaders(),c=["content-type","content-length"];Object.entries(a).forEach(([f,d])=>{c.includes(f.toLowerCase())&&o.set(f,d)})}}if(se.hasStandardBrowserEnv&&(r&&x.isFunction(r)&&(r=r(t)),r||r!==!1&&Dh(t.url))){const a=i&&l&&Uh.read(l);a&&o.set(i,a)}return t},Hh=typeof XMLHttpRequest<"u",Vh=Hh&&function(e){return new Promise(function(n,r){const i=Hd(e);let l=i.data;const o=ke.from(i.headers).normalize();let{responseType:s,onUploadProgress:a,onDownloadProgress:c}=i,f,d,h,w,m;function v(){w&&w(),m&&m(),i.cancelToken&&i.cancelToken.unsubscribe(f),i.signal&&i.signal.removeEventListener("abort",f)}let k=new XMLHttpRequest;k.open(i.method.toUpperCase(),i.url,!0),k.timeout=i.timeout;function g(){if(!k)return;const y=ke.from("getAllResponseHeaders"in k&&k.getAllResponseHeaders()),N={data:!s||s==="text"||s==="json"?k.responseText:k.response,status:k.status,statusText:k.statusText,headers:y,config:e,request:k};Bd(function(C){n(C),v()},function(C){r(C),v()},N),k=null}"onloadend"in k?k.onloadend=g:k.onreadystatechange=function(){!k||k.readyState!==4||k.status===0&&!(k.responseURL&&k.responseURL.indexOf("file:")===0)||setTimeout(g)},k.onabort=function(){k&&(r(new b("Request aborted",b.ECONNABORTED,e,k)),k=null)},k.onerror=function(S){const N=S&&S.message?S.message:"Network Error",R=new b(N,b.ERR_NETWORK,e,k);R.event=S||null,r(R),k=null},k.ontimeout=function(){let S=i.timeout?"timeout of "+i.timeout+"ms exceeded":"timeout exceeded";const N=i.transitional||Id;i.timeoutErrorMessage&&(S=i.timeoutErrorMessage),r(new b(S,N.clarifyTimeoutError?b.ETIMEDOUT:b.ECONNABORTED,e,k)),k=null},l===void 0&&o.setContentType(null),"setRequestHeader"in k&&x.forEach(o.toJSON(),function(S,N){k.setRequestHeader(N,S)}),x.isUndefined(i.withCredentials)||(k.withCredentials=!!i.withCredentials),s&&s!=="json"&&(k.responseType=i.responseType),c&&([h,m]=zi(c,!0),k.addEventListener("progress",h)),a&&k.upload&&([d,w]=zi(a),k.upload.addEventListener("progress",d),k.upload.addEventListener("loadend",w)),(i.cancelToken||i.signal)&&(f=y=>{k&&(r(!y||y.type?new Cr(null,e,k):y),k.abort(),k=null)},i.cancelToken&&i.cancelToken.subscribe(f),i.signal&&(i.signal.aborted?f():i.signal.addEventListener("abort",f)));const p=Mh(i.url);if(p&&se.protocols.indexOf(p)===-1){r(new b("Unsupported protocol "+p+":",b.ERR_BAD_REQUEST,e));return}k.send(l||null)})},Wh=(e,t)=>{const{length:n}=e=e?e.filter(Boolean):[];if(t||n){let r=new AbortController,i;const l=function(c){if(!i){i=!0,s();const f=c instanceof Error?c:this.reason;r.abort(f instanceof b?f:new Cr(f instanceof Error?f.message:f))}};let o=t&&setTimeout(()=>{o=null,l(new b(`timeout of ${t}ms exceeded`,b.ETIMEDOUT))},t);const s=()=>{e&&(o&&clearTimeout(o),o=null,e.forEach(c=>{c.unsubscribe?c.unsubscribe(l):c.removeEventListener("abort",l)}),e=null)};e.forEach(c=>c.addEventListener("abort",l));const{signal:a}=r;return a.unsubscribe=()=>x.asap(s),a}},Kh=function*(e,t){let n=e.byteLength;if(n<t){yield e;return}let r=0,i;for(;r<n;)i=r+t,yield e.slice(r,i),r=i},Qh=async function*(e,t){for await(const n of Gh(e))yield*Kh(n,t)},Gh=async function*(e){if(e[Symbol.asyncIterator]){yield*e;return}const t=e.getReader();try{for(;;){const{done:n,value:r}=await t.read();if(n)break;yield r}}finally{await t.cancel()}},qa=(e,t,n,r)=>{const i=Qh(e,t);let l=0,o,s=a=>{o||(o=!0,r&&r(a))};return new ReadableStream({async pull(a){try{const{done:c,value:f}=await i.next();if(c){s(),a.close();return}let d=f.byteLength;if(n){let h=l+=d;n(h)}a.enqueue(new Uint8Array(f))}catch(c){throw s(c),c}},cancel(a){return s(a),i.return()}},{highWaterMark:2})},Ya=64*1024,{isFunction:Kr}=x,qh=(({Request:e,Response:t})=>({Request:e,Response:t}))(x.global),{ReadableStream:Xa,TextEncoder:Ja}=x.global,Za=(e,...t)=>{try{return!!e(...t)}catch{return!1}},Yh=e=>{e=x.merge.call({skipUndefined:!0},qh,e);const{fetch:t,Request:n,Response:r}=e,i=t?Kr(t):typeof fetch=="function",l=Kr(n),o=Kr(r);if(!i)return!1;const s=i&&Kr(Xa),a=i&&(typeof Ja=="function"?(m=>v=>m.encode(v))(new Ja):async m=>new Uint8Array(await new n(m).arrayBuffer())),c=l&&s&&Za(()=>{let m=!1;const v=new n(se.origin,{body:new Xa,method:"POST",get duplex(){return m=!0,"half"}}).headers.has("Content-Type");return m&&!v}),f=o&&s&&Za(()=>x.isReadableStream(new r("").body)),d={stream:f&&(m=>m.body)};i&&["text","arrayBuffer","blob","formData","stream"].forEach(m=>{!d[m]&&(d[m]=(v,k)=>{let g=v&&v[m];if(g)return g.call(v);throw new b(`Response type '${m}' is not supported`,b.ERR_NOT_SUPPORT,k)})});const h=async m=>{if(m==null)return 0;if(x.isBlob(m))return m.size;if(x.isSpecCompliantForm(m))return(await new n(se.origin,{method:"POST",body:m}).arrayBuffer()).byteLength;if(x.isArrayBufferView(m)||x.isArrayBuffer(m))return m.byteLength;if(x.isURLSearchParams(m)&&(m=m+""),x.isString(m))return(await a(m)).byteLength},w=async(m,v)=>{const k=x.toFiniteNumber(m.getContentLength());return k??h(v)};return async m=>{let{url:v,method:k,data:g,signal:p,cancelToken:y,timeout:S,onDownloadProgress:N,onUploadProgress:R,responseType:C,headers:T,withCredentials:I="same-origin",fetchOptions:O}=Hd(m),me=t||fetch;C=C?(C+"").toLowerCase():"text";let Ke=Wh([p,y&&y.toAbortSignal()],S),Fe=null;const Qe=Ke&&Ke.unsubscribe&&(()=>{Ke.unsubscribe()});let _r;try{if(R&&c&&k!=="get"&&k!=="head"&&(_r=await w(T,g))!==0){let M=new n(v,{method:"POST",body:g,duplex:"half"}),U;if(x.isFormData(g)&&(U=M.headers.get("content-type"))&&T.setContentType(U),M.body){const[ct,be]=Ka(_r,zi(Qa(R)));g=qa(M.body,Ya,ct,be)}}x.isString(I)||(I=I?"include":"omit");const he=l&&"credentials"in n.prototype,qt={...O,signal:Ke,method:k.toUpperCase(),headers:T.normalize().toJSON(),body:g,duplex:"half",credentials:he?I:void 0};Fe=l&&new n(v,qt);let j=await(l?me(Fe,O):me(v,qt));const P=f&&(C==="stream"||C==="response");if(f&&(N||P&&Qe)){const M={};["status","statusText","headers"].forEach(Yt=>{M[Yt]=j[Yt]});const U=x.toFiniteNumber(j.headers.get("content-length")),[ct,be]=N&&Ka(U,zi(Qa(N),!0))||[];j=new r(qa(j.body,Ya,ct,()=>{be&&be(),Qe&&Qe()}),M)}C=C||"text";let z=await d[x.findKey(d,C)||"text"](j,m);return!P&&Qe&&Qe(),await new Promise((M,U)=>{Bd(M,U,{data:z,headers:ke.from(j.headers),status:j.status,statusText:j.statusText,config:m,request:Fe})})}catch(he){throw Qe&&Qe(),he&&he.name==="TypeError"&&/Load failed|fetch/i.test(he.message)?Object.assign(new b("Network Error",b.ERR_NETWORK,m,Fe),{cause:he.cause||he}):b.from(he,he&&he.code,m,Fe)}}},Xh=new Map,Vd=e=>{let t=e&&e.env||{};const{fetch:n,Request:r,Response:i}=t,l=[r,i,n];let o=l.length,s=o,a,c,f=Xh;for(;s--;)a=l[s],c=f.get(a),c===void 0&&f.set(a,c=s?new Map:Yh(t)),f=c;return c};Vd();const Ts={http:mh,xhr:Vh,fetch:{get:Vd}};x.forEach(Ts,(e,t)=>{if(e){try{Object.defineProperty(e,"name",{value:t})}catch{}Object.defineProperty(e,"adapterName",{value:t})}});const eu=e=>`- ${e}`,Jh=e=>x.isFunction(e)||e===null||e===!1;function Zh(e,t){e=x.isArray(e)?e:[e];const{length:n}=e;let r,i;const l={};for(let o=0;o<n;o++){r=e[o];let s;if(i=r,!Jh(r)&&(i=Ts[(s=String(r)).toLowerCase()],i===void 0))throw new b(`Unknown adapter '${s}'`);if(i&&(x.isFunction(i)||(i=i.get(t))))break;l[s||"#"+o]=i}if(!i){const o=Object.entries(l).map(([a,c])=>`adapter ${a} `+(c===!1?"is not supported by the environment":"is not available in the build"));let s=n?o.length>1?`since :
`+o.map(eu).join(`
`):" "+eu(o[0]):"as no adapter specified";throw new b("There is no suitable adapter to dispatch the request "+s,"ERR_NOT_SUPPORT")}return i}const Wd={getAdapter:Zh,adapters:Ts};function bl(e){if(e.cancelToken&&e.cancelToken.throwIfRequested(),e.signal&&e.signal.aborted)throw new Cr(null,e)}function tu(e){return bl(e),e.headers=ke.from(e.headers),e.data=Tl.call(e,e.transformRequest),["post","put","patch"].indexOf(e.method)!==-1&&e.headers.setContentType("application/x-www-form-urlencoded",!1),Wd.getAdapter(e.adapter||jr.adapter,e)(e).then(function(r){return bl(e),r.data=Tl.call(e,e.transformResponse,r),r.headers=ke.from(r.headers),r},function(r){return Ud(r)||(bl(e),r&&r.response&&(r.response.data=Tl.call(e,e.transformResponse,r.response),r.response.headers=ke.from(r.response.headers))),Promise.reject(r)})}const Kd="1.13.4",Zi={};["object","boolean","number","function","string","symbol"].forEach((e,t)=>{Zi[e]=function(r){return typeof r===e||"a"+(t<1?"n ":" ")+e}});const nu={};Zi.transitional=function(t,n,r){function i(l,o){return"[Axios v"+Kd+"] Transitional option '"+l+"'"+o+(r?". "+r:"")}return(l,o,s)=>{if(t===!1)throw new b(i(o," has been removed"+(n?" in "+n:"")),b.ERR_DEPRECATED);return n&&!nu[o]&&(nu[o]=!0,console.warn(i(o," has been deprecated since v"+n+" and will be removed in the near future"))),t?t(l,o,s):!0}};Zi.spelling=function(t){return(n,r)=>(console.warn(`${r} is likely a misspelling of ${t}`),!0)};function eg(e,t,n){if(typeof e!="object")throw new b("options must be an object",b.ERR_BAD_OPTION_VALUE);const r=Object.keys(e);let i=r.length;for(;i-- >0;){const l=r[i],o=t[l];if(o){const s=e[l],a=s===void 0||o(s,l,e);if(a!==!0)throw new b("option "+l+" must be "+a,b.ERR_BAD_OPTION_VALUE);continue}if(n!==!0)throw new b("Unknown option "+l,b.ERR_BAD_OPTION)}}const si={assertOptions:eg,validators:Zi},qe=si.validators;let Ut=class{constructor(t){this.defaults=t||{},this.interceptors={request:new Va,response:new Va}}async request(t,n){try{return await this._request(t,n)}catch(r){if(r instanceof Error){let i={};Error.captureStackTrace?Error.captureStackTrace(i):i=new Error;const l=i.stack?i.stack.replace(/^.+\n/,""):"";try{r.stack?l&&!String(r.stack).endsWith(l.replace(/^.+\n.+\n/,""))&&(r.stack+=`
`+l):r.stack=l}catch{}}throw r}}_request(t,n){typeof t=="string"?(n=n||{},n.url=t):n=t||{},n=Kt(this.defaults,n);const{transitional:r,paramsSerializer:i,headers:l}=n;r!==void 0&&si.assertOptions(r,{silentJSONParsing:qe.transitional(qe.boolean),forcedJSONParsing:qe.transitional(qe.boolean),clarifyTimeoutError:qe.transitional(qe.boolean)},!1),i!=null&&(x.isFunction(i)?n.paramsSerializer={serialize:i}:si.assertOptions(i,{encode:qe.function,serialize:qe.function},!0)),n.allowAbsoluteUrls!==void 0||(this.defaults.allowAbsoluteUrls!==void 0?n.allowAbsoluteUrls=this.defaults.allowAbsoluteUrls:n.allowAbsoluteUrls=!0),si.assertOptions(n,{baseUrl:qe.spelling("baseURL"),withXsrfToken:qe.spelling("withXSRFToken")},!0),n.method=(n.method||this.defaults.method||"get").toLowerCase();let o=l&&x.merge(l.common,l[n.method]);l&&x.forEach(["delete","get","head","post","put","patch","common"],m=>{delete l[m]}),n.headers=ke.concat(o,l);const s=[];let a=!0;this.interceptors.request.forEach(function(v){typeof v.runWhen=="function"&&v.runWhen(n)===!1||(a=a&&v.synchronous,s.unshift(v.fulfilled,v.rejected))});const c=[];this.interceptors.response.forEach(function(v){c.push(v.fulfilled,v.rejected)});let f,d=0,h;if(!a){const m=[tu.bind(this),void 0];for(m.unshift(...s),m.push(...c),h=m.length,f=Promise.resolve(n);d<h;)f=f.then(m[d++],m[d++]);return f}h=s.length;let w=n;for(;d<h;){const m=s[d++],v=s[d++];try{w=m(w)}catch(k){v.call(this,k);break}}try{f=tu.call(this,w)}catch(m){return Promise.reject(m)}for(d=0,h=c.length;d<h;)f=f.then(c[d++],c[d++]);return f}getUri(t){t=Kt(this.defaults,t);const n=$d(t.baseURL,t.url,t.allowAbsoluteUrls);return Fd(n,t.params,t.paramsSerializer)}};x.forEach(["delete","get","head","options"],function(t){Ut.prototype[t]=function(n,r){return this.request(Kt(r||{},{method:t,url:n,data:(r||{}).data}))}});x.forEach(["post","put","patch"],function(t){function n(r){return function(l,o,s){return this.request(Kt(s||{},{method:t,headers:r?{"Content-Type":"multipart/form-data"}:{},url:l,data:o}))}}Ut.prototype[t]=n(),Ut.prototype[t+"Form"]=n(!0)});let tg=class Qd{constructor(t){if(typeof t!="function")throw new TypeError("executor must be a function.");let n;this.promise=new Promise(function(l){n=l});const r=this;this.promise.then(i=>{if(!r._listeners)return;let l=r._listeners.length;for(;l-- >0;)r._listeners[l](i);r._listeners=null}),this.promise.then=i=>{let l;const o=new Promise(s=>{r.subscribe(s),l=s}).then(i);return o.cancel=function(){r.unsubscribe(l)},o},t(function(l,o,s){r.reason||(r.reason=new Cr(l,o,s),n(r.reason))})}throwIfRequested(){if(this.reason)throw this.reason}subscribe(t){if(this.reason){t(this.reason);return}this._listeners?this._listeners.push(t):this._listeners=[t]}unsubscribe(t){if(!this._listeners)return;const n=this._listeners.indexOf(t);n!==-1&&this._listeners.splice(n,1)}toAbortSignal(){const t=new AbortController,n=r=>{t.abort(r)};return this.subscribe(n),t.signal.unsubscribe=()=>this.unsubscribe(n),t.signal}static source(){let t;return{token:new Qd(function(i){t=i}),cancel:t}}};function ng(e){return function(n){return e.apply(null,n)}}function rg(e){return x.isObject(e)&&e.isAxiosError===!0}const To={Continue:100,SwitchingProtocols:101,Processing:102,EarlyHints:103,Ok:200,Created:201,Accepted:202,NonAuthoritativeInformation:203,NoContent:204,ResetContent:205,PartialContent:206,MultiStatus:207,AlreadyReported:208,ImUsed:226,MultipleChoices:300,MovedPermanently:301,Found:302,SeeOther:303,NotModified:304,UseProxy:305,Unused:306,TemporaryRedirect:307,PermanentRedirect:308,BadRequest:400,Unauthorized:401,PaymentRequired:402,Forbidden:403,NotFound:404,MethodNotAllowed:405,NotAcceptable:406,ProxyAuthenticationRequired:407,RequestTimeout:408,Conflict:409,Gone:410,LengthRequired:411,PreconditionFailed:412,PayloadTooLarge:413,UriTooLong:414,UnsupportedMediaType:415,RangeNotSatisfiable:416,ExpectationFailed:417,ImATeapot:418,MisdirectedRequest:421,UnprocessableEntity:422,Locked:423,FailedDependency:424,TooEarly:425,UpgradeRequired:426,PreconditionRequired:428,TooManyRequests:429,RequestHeaderFieldsTooLarge:431,UnavailableForLegalReasons:451,InternalServerError:500,NotImplemented:501,BadGateway:502,ServiceUnavailable:503,GatewayTimeout:504,HttpVersionNotSupported:505,VariantAlsoNegotiates:506,InsufficientStorage:507,LoopDetected:508,NotExtended:510,NetworkAuthenticationRequired:511,WebServerIsDown:521,ConnectionTimedOut:522,OriginIsUnreachable:523,TimeoutOccurred:524,SslHandshakeFailed:525,InvalidSslCertificate:526};Object.entries(To).forEach(([e,t])=>{To[t]=e});function Gd(e){const t=new Ut(e),n=Cd(Ut.prototype.request,t);return x.extend(n,Ut.prototype,t,{allOwnKeys:!0}),x.extend(n,t,null,{allOwnKeys:!0}),n.create=function(i){return Gd(Kt(e,i))},n}const q=Gd(jr);q.Axios=Ut;q.CanceledError=Cr;q.CancelToken=tg;q.isCancel=Ud;q.VERSION=Kd;q.toFormData=Ji;q.AxiosError=b;q.Cancel=q.CanceledError;q.all=function(t){return Promise.all(t)};q.spread=ng;q.isAxiosError=rg;q.mergeConfig=Kt;q.AxiosHeaders=ke;q.formToJSON=e=>Dd(x.isHTMLForm(e)?new FormData(e):e);q.getAdapter=Wd.getAdapter;q.HttpStatusCode=To;q.default=q;const{Axios:i0,AxiosError:l0,CanceledError:o0,isCancel:s0,CancelToken:a0,VERSION:u0,all:c0,Cancel:d0,isAxiosError:f0,spread:p0,toFormData:m0,AxiosHeaders:h0,HttpStatusCode:g0,formToJSON:y0,getAdapter:v0,mergeConfig:x0}=q,bs=q.create({baseURL:"http://localhost:8000"}),ig=async e=>{const t=await bs.post("/api/compatibility",e);return console.log("🔍 Raw compatibility API response:",JSON.stringify(t.data,null,2)),t.data},lg=async e=>{const{data:t}=await bs.post("/api/natal",e);return t},og=async e=>{const{data:t}=await bs.post("/api/natal/standard",e);return t},sg={},ru=e=>{let t;const n=new Set,r=(f,d)=>{const h=typeof f=="function"?f(t):f;if(!Object.is(h,t)){const w=t;t=d??(typeof h!="object"||h===null)?h:Object.assign({},t,h),n.forEach(m=>m(t,w))}},i=()=>t,a={setState:r,getState:i,getInitialState:()=>c,subscribe:f=>(n.add(f),()=>n.delete(f)),destroy:()=>{(sg?"production":void 0)!=="production"&&console.warn("[DEPRECATED] The `destroy` method will be unsupported in a future version. Instead use unsubscribe function returned by subscribe. Everything will be garbage-collected if store is garbage-collected."),n.clear()}},c=t=e(r,i,a);return a},ag=e=>e?ru(e):ru;var qd={exports:{}},Yd={},Xd={exports:{}},Jd={};/**
 * @license React
 * use-sync-external-store-shim.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var jn=je;function ug(e,t){return e===t&&(e!==0||1/e===1/t)||e!==e&&t!==t}var cg=typeof Object.is=="function"?Object.is:ug,dg=jn.useState,fg=jn.useEffect,pg=jn.useLayoutEffect,mg=jn.useDebugValue;function hg(e,t){var n=t(),r=dg({inst:{value:n,getSnapshot:t}}),i=r[0].inst,l=r[1];return pg(function(){i.value=n,i.getSnapshot=t,Pl(i)&&l({inst:i})},[e,n,t]),fg(function(){return Pl(i)&&l({inst:i}),e(function(){Pl(i)&&l({inst:i})})},[e]),mg(n),n}function Pl(e){var t=e.getSnapshot;e=e.value;try{var n=t();return!cg(e,n)}catch{return!0}}function gg(e,t){return t()}var yg=typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"?gg:hg;Jd.useSyncExternalStore=jn.useSyncExternalStore!==void 0?jn.useSyncExternalStore:yg;Xd.exports=Jd;var vg=Xd.exports;/**
 * @license React
 * use-sync-external-store-shim/with-selector.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */var el=je,xg=vg;function wg(e,t){return e===t&&(e!==0||1/e===1/t)||e!==e&&t!==t}var Sg=typeof Object.is=="function"?Object.is:wg,kg=xg.useSyncExternalStore,Eg=el.useRef,Ng=el.useEffect,jg=el.useMemo,Cg=el.useDebugValue;Yd.useSyncExternalStoreWithSelector=function(e,t,n,r,i){var l=Eg(null);if(l.current===null){var o={hasValue:!1,value:null};l.current=o}else o=l.current;l=jg(function(){function a(w){if(!c){if(c=!0,f=w,w=r(w),i!==void 0&&o.hasValue){var m=o.value;if(i(m,w))return d=m}return d=w}if(m=d,Sg(f,w))return m;var v=r(w);return i!==void 0&&i(m,v)?(f=w,m):(f=w,d=v)}var c=!1,f,d,h=n===void 0?null:n;return[function(){return a(t())},h===null?void 0:function(){return a(h())}]},[t,n,r,i]);var s=kg(e,l[0],l[1]);return Ng(function(){o.hasValue=!0,o.value=s},[s]),Cg(s),s};qd.exports=Yd;var _g=qd.exports;const Rg=fu(_g),Zd={},{useDebugValue:Tg}=Eu,{useSyncExternalStoreWithSelector:bg}=Rg;let iu=!1;const Pg=e=>e;function zg(e,t=Pg,n){(Zd?"production":void 0)!=="production"&&n&&!iu&&(console.warn("[DEPRECATED] Use `createWithEqualityFn` instead of `create` or use `useStoreWithEqualityFn` instead of `useStore`. They can be imported from 'zustand/traditional'. https://github.com/pmndrs/zustand/discussions/1937"),iu=!0);const r=bg(e.subscribe,e.getState,e.getServerState||e.getInitialState,t,n);return Tg(r),r}const lu=e=>{(Zd?"production":void 0)!=="production"&&typeof e!="function"&&console.warn("[DEPRECATED] Passing a vanilla store will be unsupported in a future version. Instead use `import { useStore } from 'zustand'`.");const t=typeof e=="function"?ag(e):e,n=(r,i)=>zg(t,r,i);return Object.assign(n,t),n},Og=e=>e?lu(e):lu,ae=Og(e=>({mode:"compatibility",result:null,resultType:null,loading:!1,error:null,setMode:t=>e({mode:t}),setLoading:t=>e({loading:t}),setError:t=>e({error:t}),setResult:(t,n)=>e({resultType:t,result:n,error:null,loading:!1}),reset:()=>e({result:null,resultType:null,error:null,loading:!1})})),gr={Vietnam:["Hà Nội","TP. Hồ Chí Minh","Đà Nẵng","Huế","Cần Thơ","Hải Phòng"],Thailand:["Bangkok","Chiang Mai","Phuket","Pattaya"],Singapore:["Singapore"],Japan:["Tokyo","Osaka","Kyoto","Fukuoka"],"South Korea":["Seoul","Busan","Incheon","Daegu"],USA:["New York","Los Angeles","Chicago","Houston"],France:["Paris","Lyon","Marseille","Nice"]},Ps="Vietnam";function Cn(e,t){return!e&&!t?"":t?`${t}, ${e}`:e}function tl(e=Ps){var t;return((t=gr[e])==null?void 0:t[0])||""}/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Lg=e=>e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase(),ef=(...e)=>e.filter((t,n,r)=>!!t&&r.indexOf(t)===n).join(" ");/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */var Ag={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:2,strokeLinecap:"round",strokeLinejoin:"round"};/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Mg=je.forwardRef(({color:e="currentColor",size:t=24,strokeWidth:n=2,absoluteStrokeWidth:r,className:i="",children:l,iconNode:o,...s},a)=>je.createElement("svg",{ref:a,...Ag,width:t,height:t,stroke:e,strokeWidth:r?Number(n)*24/Number(t):n,className:ef("lucide",i),...s},[...o.map(([c,f])=>je.createElement(c,f)),...Array.isArray(l)?l:[l]]));/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const tf=(e,t)=>{const n=je.forwardRef(({className:r,...i},l)=>je.createElement(Mg,{ref:l,iconNode:t,className:ef(`lucide-${Lg(e)}`,r),...i}));return n.displayName=`${e}`,n};/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Fg=tf("Heart",[["path",{d:"M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z",key:"c3ymky"}]]);/**
 * @license lucide-react v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ig=tf("Sparkles",[["path",{d:"M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z",key:"4pj2yx"}],["path",{d:"M20 3v4",key:"1olli1"}],["path",{d:"M22 5h-4",key:"1gvqau"}],["path",{d:"M4 17v2",key:"vumght"}],["path",{d:"M5 18H3",key:"zchphs"}]]),bo=Ps,ou=tl(bo),su={name:"",gender:"other",birth_date:"",birth_time:"",time_unknown:!1,country:bo,city:ou,birth_place:Cn(bo,ou)};function au({title:e,person:t,onChange:n}){const r=Object.keys(gr),i=gr[t.country]||[],l=s=>{const a=tl(s);n({...t,country:s,city:a,birth_place:Cn(s,a)})},o=s=>{n({...t,city:s,birth_place:Cn(t.country,s)})};return u.jsxs("div",{className:"glass-card person-card",children:[u.jsxs("h3",{className:"card-title",children:[u.jsx(Ig,{className:"icon-nebula"}),e]}),u.jsxs("div",{className:"form-grid",children:[u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Tên (Biệt danh)"}),u.jsx("input",{className:"glass-input",value:t.name,onChange:s=>n({...t,name:s.target.value}),placeholder:"Nhập tên..."})]}),u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Giới tính"}),u.jsxs("select",{className:"glass-input",value:t.gender,onChange:s=>n({...t,gender:s.target.value}),children:[u.jsx("option",{value:"female",children:"Nữ"}),u.jsx("option",{value:"male",children:"Nam"}),u.jsx("option",{value:"other",children:"Khác"})]})]}),u.jsxs("div",{className:"form-row",children:[u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Ngày sinh"}),u.jsx("input",{type:"date",className:"glass-input",value:t.birth_date,onChange:s=>n({...t,birth_date:s.target.value})})]}),u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Giờ sinh"}),u.jsx("input",{type:"time",className:"glass-input",value:t.birth_time,onChange:s=>n({...t,birth_time:s.target.value}),disabled:t.time_unknown}),u.jsxs("label",{className:"checkbox-label",children:[u.jsx("input",{type:"checkbox",checked:t.time_unknown,onChange:s=>n({...t,time_unknown:s.target.checked})}),u.jsx("span",{children:"Không rõ giờ sinh"})]})]})]}),u.jsxs("div",{className:"form-row",children:[u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Quốc gia"}),u.jsx("select",{className:"glass-input",value:t.country,onChange:s=>l(s.target.value),children:r.map(s=>u.jsx("option",{value:s,children:s},s))})]}),u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Thành phố"}),u.jsx("select",{className:"glass-input",value:t.city,onChange:s=>o(s.target.value),children:i.map(s=>u.jsx("option",{value:s,children:s},s))})]})]})]})]})}function uu(e){return{name:e.name,gender:e.gender,birth_date:e.birth_date,birth_time:e.birth_time,time_unknown:e.time_unknown,birth_place:e.birth_place}}function Dg(){const[e,t]=je.useState(su),[n,r]=je.useState(su),i=ae(a=>a.setLoading),l=ae(a=>a.setError),o=ae(a=>a.setResult),s=async a=>{var c,f;a.preventDefault(),i(!0),l(null);try{const d={person_a:uu(e),person_b:uu(n)},h=await ig(d);o("compatibility",h)}catch(d){l(((f=(c=d==null?void 0:d.response)==null?void 0:c.data)==null?void 0:f.detail)||"Đã có lỗi xảy ra"),i(!1)}};return u.jsxs("div",{className:"compatibility-form-wrapper",children:[u.jsxs("div",{className:"form-header",children:[u.jsx("h2",{className:"title-gradient",children:"Kết Nối Vì Sao"}),u.jsx("p",{className:"desc",children:"Khám phá sự hòa hợp giữa hai tâm hồn thông qua lăng kính chiêm tinh học."})]}),u.jsxs("form",{onSubmit:s,className:"comp-form",children:[u.jsxs("div",{className:"comp-grid",children:[u.jsx("div",{className:"connector-overlay",children:u.jsx("div",{className:"heart-circle",children:u.jsx(Fg,{className:"icon-heart"})})}),u.jsx(au,{title:"Bạn",person:e,onChange:t}),u.jsx(au,{title:"Đối phương",person:n,onChange:r})]}),u.jsx("div",{className:"submit-area",children:u.jsx("button",{type:"submit",className:"btn-cosmic main-submit",children:"Xem Kết Quả Tương Hợp"})})]}),u.jsx("style",{children:`
        .compatibility-form-wrapper {
          padding: 20px 0;
        }
        .form-header {
          text-align: center;
          margin-bottom: 50px;
        }
        .title-gradient {
          font-size: 3rem;
          margin-bottom: 12px;
          background: linear-gradient(135deg, var(--gold-primary), var(--nebula-pink));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .desc {
          color: var(--white-70);
          max-width: 600px;
          margin: 0 auto;
        }
        .comp-form {
          position: relative;
        }
        .comp-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 40px;
          position: relative;
        }
        .submit-area {
          display: flex;
          justify-content: center;
          margin-top: 50px;
        }
        .main-submit {
          min-width: 300px;
          font-size: 1.1rem;
        }
        .card-title {
          font-size: 1.5rem;
          margin-bottom: 24px;
          display: flex;
          align-items: center;
          gap: 12px;
          color: var(--gold-primary);
        }
        .icon-nebula {
          color: var(--nebula-purple);
        }
        .form-grid {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        .form-field {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .form-field label {
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 1px;
          color: var(--white-40);
        }
        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }
        .checkbox-label {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-top: 8px;
          font-size: 12px;
          color: var(--white-70);
          cursor: pointer;
        }
        .connector-overlay {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          z-index: 5;
        }
        .heart-circle {
          width: 50px;
          height: 50px;
          background: var(--space-ink);
          border: 1px solid var(--white-10);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 0 20px var(--nebula-purple-glow);
        }
        .icon-heart {
          color: var(--nebula-pink);
          fill: rgba(217, 70, 239, 0.2);
        }

        @media (max-width: 992px) {
          .comp-grid {
            grid-template-columns: 1fr;
            gap: 24px;
          }
          .connector-overlay {
            display: none;
          }
        }
      `})]})}const Po=Ps,cu=tl(Po),Ug={name:"",gender:"other",birth_date:"",birth_time:"",time_unknown:!1,country:Po,city:cu,birth_place:Cn(Po,cu)};function Bg(){const[e,t]=je.useState(Ug),n=ae(d=>d.mode),r=ae(d=>d.setLoading),i=ae(d=>d.setError),l=ae(d=>d.setResult),o=Object.keys(gr),s=gr[e.country]||[],a=d=>{const h=tl(d);t({...e,country:d,city:h,birth_place:Cn(d,h)})},c=d=>{t({...e,city:d,birth_place:Cn(e.country,d)})},f=async d=>{var h,w;d.preventDefault(),r(!0),i(null);try{if(n==="standard"){const m={person:{name:e.name,gender:e.gender,birth_date:e.birth_date,birth_time:e.birth_time,time_unknown:e.time_unknown,birth_place:e.birth_place}},v=await og(m);l("standard",v)}else{const m={person:{name:e.name,gender:e.gender,birth_date:e.birth_date,birth_time:e.birth_time,time_unknown:e.time_unknown,birth_place:e.birth_place}},v=await lg(m);l("natal",v)}}catch(m){i(((w=(h=m==null?void 0:m.response)==null?void 0:h.data)==null?void 0:w.detail)||"Đã có lỗi xảy ra"),r(!1)}};return u.jsxs("form",{onSubmit:f,className:"single-form-wrapper animate-fade-in",children:[u.jsxs("div",{className:"glass-card person-card",children:[u.jsx("h3",{className:"card-title",children:"Hồ sơ cá nhân"}),u.jsxs("div",{className:"form-grid",children:[u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Tên (không bắt buộc)"}),u.jsx("input",{className:"glass-input",value:e.name,onChange:d=>t({...e,name:d.target.value}),placeholder:"Ví dụ: Linh"})]}),u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Giới tính"}),u.jsxs("select",{className:"glass-input",value:e.gender,onChange:d=>t({...e,gender:d.target.value}),children:[u.jsx("option",{value:"female",children:"Nữ"}),u.jsx("option",{value:"male",children:"Nam"}),u.jsx("option",{value:"other",children:"Khác"})]})]}),u.jsxs("div",{className:"form-row",children:[u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Ngày sinh"}),u.jsx("input",{type:"date",className:"glass-input",value:e.birth_date,onChange:d=>t({...e,birth_date:d.target.value})})]}),u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Giờ sinh"}),u.jsx("input",{type:"time",className:"glass-input",value:e.birth_time,onChange:d=>t({...e,birth_time:d.target.value}),disabled:e.time_unknown}),u.jsxs("label",{className:"checkbox-label",children:[u.jsx("input",{type:"checkbox",checked:e.time_unknown,onChange:d=>t({...e,time_unknown:d.target.checked})}),u.jsx("span",{children:"Không rõ giờ sinh"})]})]})]}),u.jsxs("div",{className:"form-row",children:[u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Quốc gia"}),u.jsx("select",{className:"glass-input",value:e.country,onChange:d=>a(d.target.value),children:o.map(d=>u.jsx("option",{value:d,children:d},d))})]}),u.jsxs("div",{className:"form-field",children:[u.jsx("label",{children:"Thành phố"}),u.jsx("select",{className:"glass-input",value:e.city,onChange:d=>c(d.target.value),children:s.map(d=>u.jsx("option",{value:d,children:d},d))})]})]})]})]}),u.jsx("div",{className:"submit-area",children:u.jsx("button",{type:"submit",className:"btn-cosmic main-submit",children:"Giải Mã Bản Đồ Sao"})}),u.jsx("style",{children:`
        .single-form-wrapper {
          max-width: 600px;
          margin: 0 auto;
        }
        .submit-area {
          display: flex;
          justify-content: center;
          margin-top: 40px;
        }
        .main-submit {
          min-width: 250px;
        }
        .card-title {
          font-size: 1.5rem;
          margin-bottom: 24px;
          color: var(--gold-primary);
          font-family: var(--font-display);
        }
        .form-grid {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }
        .form-field {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .form-field label {
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 1px;
          color: var(--white-40);
        }
        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }
        .checkbox-label {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-top: 8px;
          font-size: 12px;
          color: var(--white-70);
          cursor: pointer;
        }
      `})]})}function $g(){const e=ae(l=>l.loading),t=ae(l=>l.error),n=ae(l=>l.setError),r=ae(l=>l.mode),i=ae(l=>l.setMode);return u.jsxs("div",{className:"home-page section-py",children:[u.jsx("header",{className:"container",children:u.jsxs("div",{className:"hero-content",children:[u.jsx("p",{className:"subtitle",children:"Khám phá Bản đồ sao"}),u.jsx("h1",{className:"main-title",children:"Khám phá sự tương hợp và năng lượng vũ trụ của bạn."}),u.jsx("p",{className:"hero-desc",children:"Nhập thông tin sinh để nhận bản phân tích chi tiết về Mặt Trời, Mặt Trăng, Cung mọc và chỉ số tương hợp."})]})}),u.jsxs("main",{className:"container",children:[u.jsxs("div",{className:"mode-selector-header",children:[u.jsx("h2",{className:"section-title",children:"Chọn loại tra cứu"}),e&&u.jsx("span",{className:"loading-status",children:"Đang tính toán..."})]}),u.jsxs("div",{className:"mode-tabs",children:[u.jsx("button",{type:"button",className:`btn-outline ${r==="compatibility"?"active":""}`,onClick:()=>i("compatibility"),children:"Tương hợp 2 người"}),u.jsx("button",{type:"button",className:`btn-outline ${r==="natal"?"active":""}`,onClick:()=>i("natal"),children:"Tra cứu 1 người"}),u.jsx("button",{type:"button",className:`btn-outline ${r==="standard"?"active":""}`,onClick:()=>i("standard"),children:"Báo cáo chuẩn"})]}),t&&u.jsx("div",{className:"error-box glass-card",children:u.jsxs("div",{className:"error-content",children:[u.jsx("span",{children:typeof t=="string"?t:JSON.stringify(t)}),u.jsx("button",{className:"btn-close",onClick:()=>n(null),children:"Đóng"})]})}),u.jsx("div",{className:"form-container",children:r==="compatibility"?u.jsx(Dg,{}):u.jsx(Bg,{})})]}),u.jsx("style",{children:`
        .hero-content {
          max-width: 800px;
          margin-bottom: 60px;
        }
        .subtitle {
          color: var(--nebula-pink);
          text-transform: uppercase;
          letter-spacing: 4px;
          font-size: 14px;
          font-weight: 600;
          margin-bottom: 16px;
        }
        .main-title {
          font-size: 3.5rem;
          line-height: 1.1;
          margin-bottom: 24px;
          background: linear-gradient(to right, #fff, var(--gold-primary));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .hero-desc {
          font-size: 1.1rem;
          color: var(--white-70);
          max-width: 600px;
        }
        .mode-selector-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
        }
        .mode-tabs {
          display: flex;
          gap: 16px;
          margin-bottom: 40px;
        }
        .loading-status {
          color: var(--nebula-purple);
          font-size: 0.9rem;
          font-weight: 600;
        }
        .error-box {
          margin-bottom: 32px;
          padding: 16px 24px;
          border-left: 4px solid #ef4444;
          background: rgba(239, 68, 68, 0.1);
        }
        .error-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .btn-close {
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          text-decoration: underline;
        }
      `})]})}const Hg=({report:e,chartData:t,generatedAt:n})=>{const i=(o=>{const s=[],a=o.split(`
`);let c=null,f=[];for(const d of a){const h=d.trim(),w=h.match(/^(\d+)\.\s+(.+)$/);w?(c&&(c.content=f,s.push(c)),c={id:w[1],title:w[2],content:[]},f=[]):c&&h&&f.push(h)}return c&&(c.content=f,s.push(c)),s})(e),l=o=>o.includes("Tổng quan")?"📊":o.includes("Nhân dạng")?"👤":o.includes("Tình yêu")?"❤️":o.includes("Thế hệ")?"🌍":o.includes("Bài học")?"🎓":o.includes("Kết luận")?"🎯":"📄";return u.jsxs("div",{className:"standard-report-container",children:[u.jsxs("div",{className:"report-header",children:[u.jsxs("div",{className:"header-badge",children:[u.jsx("span",{className:"report-icon",children:"📜"}),u.jsx("span",{className:"report-type",children:"BÁO CÁO CHUẨN"})]}),u.jsx("h1",{className:"report-title",children:"BÁO CÁO CHIẾM TINH CHUẨN"}),u.jsxs("div",{className:"chart-info",children:[u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Mặt Trời"}),u.jsx("span",{children:(t==null?void 0:t.sun_sign)||"Unknown"})]}),u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Mặt Trăng"}),u.jsx("span",{children:(t==null?void 0:t.moon_sign)||"Unknown"})]}),u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Cung Mọc"}),u.jsx("span",{children:(t==null?void 0:t.ascendant)||"Unknown"})]})]}),u.jsx("div",{className:"generated-info",children:u.jsxs("span",{className:"generated-text",children:["Generated: ",new Date(n).toLocaleString("vi-VN")]})})]}),u.jsx("div",{className:"report-content",children:i.map((o,s)=>u.jsxs("div",{className:"report-section",children:[u.jsxs("div",{className:"section-header",children:[u.jsxs("div",{className:"section-title-wrapper",children:[u.jsx("span",{className:"section-icon",children:l(o.title)}),u.jsx("h2",{className:"section-title",children:o.title})]}),u.jsxs("div",{className:"section-number",children:["Phần ",o.id]})]}),u.jsx("div",{className:"section-content",children:o.content.map((a,c)=>a.startsWith("☉")||a.startsWith("☽")||a.startsWith("☿")||a.startsWith("♀")||a.startsWith("♂")||a.startsWith("☊")||a.startsWith("⚷")?u.jsxs("div",{className:"planet-header",children:[u.jsx("span",{className:"planet-symbol",children:a.split(" ")[0]}),u.jsx("span",{className:"planet-text",children:a.substring(a.indexOf(" ")+1)})]},c):a.startsWith("⚠️")?u.jsxs("div",{className:"warning-block",children:[u.jsx("span",{className:"warning-icon",children:"⚠️"}),u.jsx("span",{className:"warning-text",children:a.substring(2)})]},c):a.startsWith("👉")?u.jsxs("div",{className:"insight-block",children:[u.jsx("span",{className:"insight-icon",children:"👉"}),u.jsx("span",{className:"insight-text",children:a.substring(2)})]},c):a.startsWith("-")?u.jsxs("div",{className:"bullet-point",children:[u.jsx("span",{className:"bullet",children:"•"}),u.jsx("span",{className:"bullet-text",children:a.substring(2)})]},c):a.includes("→")?u.jsx("div",{className:"formula-block",children:u.jsx("span",{className:"formula-text",children:a})},c):u.jsx("div",{className:"normal-line",children:a},c))})]},s))}),u.jsxs("div",{className:"report-footer",children:[u.jsx("p",{className:"footer-note",children:"Báo cáo được tạo bởi hệ thống Zodiac AI. Kết quả mang tính chất tham khảo và phản ánh xu hướng năng lượng chiêm tinh."}),u.jsxs("div",{className:"footer-actions",children:[u.jsx("button",{className:"btn-secondary",onClick:()=>window.print(),children:"In Báo Cáo"}),u.jsx("button",{className:"btn-secondary",onClick:()=>{navigator.clipboard.writeText(e)},children:"Sao Chép"})]})]}),u.jsx("style",{children:`
        .standard-report-container {
          max-width: 800px;
          margin: 0 auto;
          background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 16px;
          padding: 40px;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          line-height: 1.6;
          color: #ffffff;
        }

        .report-header {
          border-bottom: 1px solid rgba(255,255,255,0.1);
          padding-bottom: 30px;
          margin-bottom: 40px;
        }

        .header-badge {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
        }

        .report-icon {
          font-size: 2rem;
        }

        .report-type {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 2px;
          color: #94a3b8;
          font-weight: 700;
        }

        .report-title {
          font-size: 2.5rem;
          margin-bottom: 24px;
          background: linear-gradient(to right, #ffffff, #9333ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          font-family: 'Georgia', serif;
          font-weight: 800;
        }

        .chart-info {
          display: flex;
          flex-wrap: wrap;
          gap: 32px;
          margin-bottom: 20px;
        }

        .info-item {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .info-item label {
          font-size: 11px;
          color: #94a3b8;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .info-item span {
          font-size: 1.2rem;
          font-weight: 600;
          color: #ffffff;
          font-family: 'Georgia', serif;
        }

        .generated-info {
          background: rgba(255,255,255,0.05);
          padding: 8px 16px;
          border-radius: 20px;
          display: inline-block;
        }

        .generated-text {
          font-size: 12px;
          color: #94a3b8;
        }

        .report-content {
          margin-bottom: 40px;
        }

        .report-section {
          margin-bottom: 40px;
          padding: 24px;
          background: rgba(255,255,255,0.02);
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.05);
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          padding-bottom: 15px;
          border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .section-title-wrapper {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .section-icon {
          font-size: 1.5rem;
        }

        .section-title {
          font-size: 1.5rem;
          margin: 0;
          color: #f472b6;
          font-family: 'Georgia', serif;
          font-weight: 700;
        }

        .section-number {
          font-size: 12px;
          color: #94a3b8;
          text-transform: uppercase;
          letter-spacing: 1px;
          font-weight: 700;
        }

        .section-content {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .planet-header {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px;
          background: rgba(147, 51, 234, 0.1);
          border-left: 3px solid #9333ea;
          border-radius: 6px;
        }

        .planet-symbol {
          font-size: 1.5rem;
          font-weight: bold;
        }

        .planet-text {
          font-size: 1rem;
          font-weight: 500;
          color: #e0e7ff;
        }

        .warning-block {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          background: rgba(245, 158, 11, 0.1);
          border-left: 3px solid #f59e0b;
          border-radius: 6px;
        }

        .warning-icon {
          font-size: 1.2rem;
          margin-top: 2px;
        }

        .warning-text {
          font-size: 0.95rem;
          color: #fde68a;
        }

        .insight-block {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          background: rgba(59, 130, 246, 0.1);
          border-left: 3px solid #3b82f6;
          border-radius: 6px;
        }

        .insight-icon {
          font-size: 1.2rem;
          margin-top: 2px;
        }

        .insight-text {
          font-size: 0.95rem;
          color: #bfdbfe;
        }

        .bullet-point {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 8px 12px;
          margin-left: 20px;
        }

        .bullet {
          color: #9333ea;
          font-weight: bold;
          margin-top: 2px;
        }

        .bullet-text {
          font-size: 0.95rem;
          color: #e5e7eb;
          line-height: 1.5;
        }

        .formula-block {
          padding: 12px;
          background: rgba(34, 197, 94, 0.1);
          border-left: 3px solid #22c55e;
          border-radius: 6px;
          margin-left: 20px;
        }

        .formula-text {
          font-size: 0.95rem;
          color: #bbf7d0;
          font-style: italic;
        }

        .normal-line {
          font-size: 0.95rem;
          color: #e5e7eb;
          line-height: 1.6;
        }

        .report-footer {
          border-top: 1px solid rgba(255,255,255,0.1);
          padding-top: 30px;
          text-align: center;
        }

        .footer-note {
          font-size: 12px;
          color: #94a3b8;
          margin-bottom: 20px;
          line-height: 1.5;
        }

        .footer-actions {
          display: flex;
          justify-content: center;
          gap: 16px;
        }

        .btn-secondary {
          background: rgba(255,255,255,0.1);
          border: 1px solid rgba(255,255,255,0.2);
          color: white;
          padding: 8px 24px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 1px;
          transition: all 0.3s ease;
        }

        .btn-secondary:hover {
          background: rgba(255,255,255,0.2);
          border-color: rgba(255,255,255,0.4);
        }

        @media (max-width: 768px) {
          .standard-report-container {
            padding: 20px;
            margin: 0 16px 40px 16px;
          }
          
          .report-title {
            font-size: 2rem;
          }
          
          .chart-info {
            gap: 16px;
          }
          
          .report-section {
            padding: 16px;
          }
          
          .section-title {
            font-size: 1.25rem;
          }
        }
      `})]})},Vg=({report:e,chartData:t,generatedAt:n,placements:r})=>{var a,c,f,d;const l=(h=>{const w=[],m=h.split(`
`);let v=null,k=[],g=!1;for(const p of m){const y=p.trim(),S=y.match(/^(\d+)\.\s+(.+)$/);S?(v&&(v.content=k,w.push(v)),v={id:S[1],title:S[2],content:[]},k=[],g=!0):g&&v&&y&&k.push(y)}return v&&(v.content=k,w.push(v)),w})(e),o=h=>h.includes("Tổng quan")?"📊":h.includes("Nhân dạng")?"👤":h.includes("Tình yêu")?"❤️":h.includes("Thế hệ")?"🌍":h.includes("Bài học")?"🎓":h.includes("Kết luận")?"🎯":"📄",s=h=>h.includes("Tổng quan")?"#3b82f6":h.includes("Nhân dạng")?"#10b981":h.includes("Tình yêu")?"#ef4444":h.includes("Thế hệ")?"#8b5cf6":h.includes("Bài học")?"#f59e0b":h.includes("Kết luận")?"#06b6d4":"#6b7280";return u.jsxs("div",{className:"zodiac-ai-container",children:[u.jsxs("div",{className:"zodiac-ai-header",children:[u.jsxs("div",{className:"header-badge",children:[u.jsx("span",{className:"ai-icon",children:"🤖"}),u.jsx("span",{className:"ai-type",children:"ZODIAC AI PROFESSIONAL"})]}),u.jsx("h1",{className:"ai-title",children:"BÁO CÁO CHIẾM TINH CHUYÊN NGHIỆP"}),u.jsx("div",{className:"ai-chart-info",children:u.jsxs("div",{className:"info-grid",children:[u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Mặt Trời"}),u.jsx("span",{children:((a=t==null?void 0:t.Sun)==null?void 0:a.sign)||"Unknown"})]}),u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Mặt Trăng"}),u.jsx("span",{children:((c=t==null?void 0:t.Moon)==null?void 0:c.sign)||"Unknown"})]}),u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Sao Kim"}),u.jsx("span",{children:((f=t==null?void 0:t.Venus)==null?void 0:f.sign)||"Unknown"})]}),u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Sao Hỏa"}),u.jsx("span",{children:((d=t==null?void 0:t.Mars)==null?void 0:d.sign)||"Unknown"})]})]})}),u.jsx("div",{className:"ai-generated-info",children:u.jsxs("span",{className:"generated-text",children:["Generated: ",new Date(n).toLocaleString("vi-VN")]})})]}),u.jsx("div",{className:"zodiac-ai-content",children:l.map((h,w)=>u.jsxs("div",{className:"ai-section",style:{borderColor:s(h.title)},children:[u.jsxs("div",{className:"ai-section-header",style:{backgroundColor:s(h.title)},children:[u.jsxs("div",{className:"section-title-wrapper",children:[u.jsx("span",{className:"section-icon",children:o(h.title)}),u.jsx("h2",{className:"ai-section-title",children:h.title})]}),u.jsxs("div",{className:"section-number",children:["Phần ",h.id]})]}),u.jsx("div",{className:"ai-section-content",children:h.content.map((m,v)=>{if(m.startsWith("☉")||m.startsWith("☽")||m.startsWith("☿")||m.startsWith("♀")||m.startsWith("♂")||m.startsWith("☊")||m.startsWith("⚷"))return u.jsxs("div",{className:"ai-planet-header",children:[u.jsx("span",{className:"ai-planet-symbol",children:m.split(" ")[0]}),u.jsx("span",{className:"ai-planet-text",children:m.substring(m.indexOf(" ")+1)})]},v);if(m.startsWith("**")&&m.endsWith("**")){const k=m.slice(2,-2);return u.jsx("div",{className:"ai-bold-header",children:k},v)}else{if(m.startsWith("⚠️"))return u.jsxs("div",{className:"ai-warning-block",children:[u.jsx("span",{className:"ai-warning-icon",children:"⚠️"}),u.jsx("span",{className:"ai-warning-text",children:m.substring(2)})]},v);if(m.startsWith("👉"))return u.jsxs("div",{className:"ai-insight-block",children:[u.jsx("span",{className:"ai-insight-icon",children:"👉"}),u.jsx("span",{className:"ai-insight-text",children:m.substring(2)})]},v);if(m.startsWith("-"))return u.jsxs("div",{className:"ai-bullet-point",children:[u.jsx("span",{className:"ai-bullet",children:"•"}),u.jsx("span",{className:"ai-bullet-text",children:m.substring(2)})]},v);if(m.includes("→"))return u.jsx("div",{className:"ai-formula-block",children:u.jsx("span",{className:"ai-formula-text",children:m})},v);if(m.includes(":")){const[k,...g]=m.split(":"),p=g.join(":");return u.jsxs("div",{className:"ai-key-value",children:[u.jsxs("span",{className:"ai-key",children:[k,":"]}),u.jsx("span",{className:"ai-value",children:p})]},v)}else return u.jsx("div",{className:"ai-normal-line",children:m},v)}})})]},w))}),u.jsxs("div",{className:"zodiac-ai-footer",children:[u.jsx("p",{className:"ai-footer-note",children:"Báo cáo được tạo bởi hệ thống Zodiac AI chuyên nghiệp. Kết quả mang tính chất tham khảo và phản ánh xu hướng năng lượng chiêm tinh."}),u.jsxs("div",{className:"ai-footer-actions",children:[u.jsx("button",{className:"btn-secondary",onClick:()=>window.print(),children:"In Báo Cáo"}),u.jsx("button",{className:"btn-secondary",onClick:()=>{navigator.clipboard.writeText(e)},children:"Sao Chép"})]})]}),u.jsx("style",{children:`
        .zodiac-ai-container {
          max-width: 900px;
          margin: 0 auto;
          background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
          border: 2px solid rgba(255,255,255,0.1);
          border-radius: 20px;
          padding: 40px;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          line-height: 1.6;
          color: #ffffff;
          box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }

        .zodiac-ai-header {
          border-bottom: 2px solid rgba(255,255,255,0.1);
          padding-bottom: 30px;
          margin-bottom: 40px;
        }

        .header-badge {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
        }

        .ai-icon {
          font-size: 2.5rem;
          filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
        }

        .ai-type {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 3px;
          color: #94a3b8;
          font-weight: 800;
          background: linear-gradient(135deg, #ffffff, #9333ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .ai-title {
          font-size: 3rem;
          margin-bottom: 24px;
          background: linear-gradient(to right, #ffffff, #9333ea, #f59e0b);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          font-family: 'Georgia', serif;
          font-weight: 800;
          text-shadow: 0 4px 20px rgba(147, 51, 234, 0.3);
        }

        .ai-chart-info {
          margin-bottom: 20px;
        }

        .info-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;
        }

        .info-item {
          background: rgba(255,255,255,0.05);
          padding: 16px;
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.1);
          text-align: center;
        }

        .info-item label {
          font-size: 11px;
          color: #94a3b8;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 8px;
          display: block;
        }

        .info-item span {
          font-size: 1.5rem;
          font-weight: 700;
          color: #ffffff;
          font-family: 'Georgia', serif;
        }

        .ai-generated-info {
          background: rgba(255,255,255,0.05);
          padding: 12px 20px;
          border-radius: 25px;
          display: inline-block;
          border: 1px solid rgba(255,255,255,0.2);
        }

        .ai-generated-text {
          font-size: 12px;
          color: #94a3b8;
        }

        .zodiac-ai-content {
          margin-bottom: 40px;
        }

        .ai-section {
          margin-bottom: 30px;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 10px 30px rgba(0,0,0,0.2);
          transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .ai-section:hover {
          transform: translateY(-2px);
          box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }

        .ai-section-header {
          padding: 20px 24px;
          color: white;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-weight: 700;
          position: relative;
          overflow: hidden;
        }

        .ai-section-header::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
          pointer-events: none;
        }

        .section-title-wrapper {
          display: flex;
          align-items: center;
          gap: 12px;
          position: relative;
          z-index: 1;
        }

        .section-icon {
          font-size: 1.5rem;
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }

        .ai-section-title {
          font-size: 1.5rem;
          margin: 0;
          font-family: 'Georgia', serif;
          font-weight: 700;
          text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }

        .section-number {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 1px;
          font-weight: 800;
          background: rgba(255,255,255,0.2);
          padding: 6px 12px;
          border-radius: 20px;
          position: relative;
          z-index: 1;
        }

        .ai-section-content {
          padding: 24px;
          background: rgba(255,255,255,0.02);
          border-top: 1px solid rgba(255,255,255,0.1);
        }

        .ai-planet-header {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px;
          background: rgba(147, 51, 234, 0.15);
          border-left: 4px solid #9333ea;
          border-radius: 8px;
          margin-bottom: 12px;
        }

        .ai-planet-symbol {
          font-size: 1.5rem;
          font-weight: bold;
          filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        }

        .ai-planet-text {
          font-size: 1rem;
          font-weight: 600;
          color: #e0e7ff;
        }

        .ai-bold-header {
          font-size: 1.1rem;
          font-weight: 700;
          color: #f8fafc;
          margin: 16px 0 8px 0;
          padding: 8px 0;
          border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .ai-warning-block {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          background: rgba(245, 158, 11, 0.15);
          border-left: 4px solid #f59e0b;
          border-radius: 8px;
          margin: 12px 0;
        }

        .ai-warning-icon {
          font-size: 1.2rem;
          margin-top: 2px;
        }

        .ai-warning-text {
          font-size: 0.95rem;
          color: #fde68a;
          font-weight: 600;
        }

        .ai-insight-block {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          background: rgba(59, 130, 246, 0.15);
          border-left: 4px solid #3b82f6;
          border-radius: 8px;
          margin: 12px 0;
        }

        .ai-insight-icon {
          font-size: 1.2rem;
          margin-top: 2px;
        }

        .ai-insight-text {
          font-size: 0.95rem;
          color: #bfdbfe;
          font-weight: 600;
        }

        .ai-bullet-point {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 8px 12px;
          margin: 8px 0;
          background: rgba(255,255,255,0.05);
          border-radius: 6px;
        }

        .ai-bullet {
          color: #9333ea;
          font-weight: bold;
          margin-top: 4px;
          font-size: 1.2rem;
        }

        .ai-bullet-text {
          font-size: 0.95rem;
          color: #e5e7eb;
          line-height: 1.5;
        }

        .ai-formula-block {
          padding: 12px;
          background: rgba(34, 197, 94, 0.15);
          border-left: 4px solid #22c55e;
          border-radius: 8px;
          margin: 12px 0;
        }

        .ai-formula-text {
          font-size: 0.95rem;
          color: #bbf7d0;
          font-style: italic;
          font-weight: 600;
        }

        .ai-key-value {
          display: flex;
          gap: 12px;
          padding: 8px 0;
          border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .ai-key {
          font-weight: 700;
          color: #9333ea;
          min-width: 120px;
          font-size: 0.9rem;
        }

        .ai-value {
          color: #e5e7eb;
          font-size: 0.95rem;
        }

        .ai-normal-line {
          font-size: 0.95rem;
          color: #e5e7eb;
          line-height: 1.6;
          margin: 8px 0;
        }

        .zodiac-ai-footer {
          border-top: 2px solid rgba(255,255,255,0.1);
          padding-top: 30px;
          text-align: center;
        }

        .ai-footer-note {
          font-size: 12px;
          color: #94a3b8;
          margin-bottom: 20px;
          line-height: 1.5;
          max-width: 700px;
          margin-left: auto;
          margin-right: auto;
        }

        .ai-footer-actions {
          display: flex;
          justify-content: center;
          gap: 16px;
        }

        .btn-secondary {
          background: rgba(255,255,255,0.1);
          border: 1px solid rgba(255,255,255,0.2);
          color: white;
          padding: 10px 24px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 12px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 1px;
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
        }

        .btn-secondary:hover {
          background: rgba(255,255,255,0.2);
          border-color: rgba(255,255,255,0.4);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        @media (max-width: 768px) {
          .zodiac-ai-container {
            padding: 20px;
            margin: 0 16px 40px 16px;
          }
          
          .ai-title {
            font-size: 2.5rem;
          }
          
          .info-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
          }
          
          .ai-section {
            margin-bottom: 20px;
          }
          
          .ai-section-title {
            font-size: 1.25rem;
          }
        }
      `})]})},Wg=({meta:e})=>{const t={Fire:"🔥",Earth:"🌿",Air:"🌬️",Water:"💧"};return u.jsxs("div",{className:`result-header-box element-${e.zodiac.element.toLowerCase()}`,children:[u.jsxs("div",{className:"header-badge",children:[u.jsx("span",{className:"element-icon",children:t[e.zodiac.element]}),u.jsx("span",{className:"chart-type",children:e.chartType==="with_birth_time"?"Bản đồ đầy đủ":"Bản đồ cơ bản"})]}),u.jsx("h1",{className:"header-title",children:"Hồ Sơ Chiêm Tinh"}),u.jsxs("div",{className:"zodiac-info-grid",children:[u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Mặt Trời"}),u.jsx("span",{children:e.zodiac.sun})]}),e.zodiac.moon&&u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Mặt Trăng"}),u.jsx("span",{children:e.zodiac.moon})]}),e.zodiac.rising&&u.jsxs("div",{className:"info-item",children:[u.jsx("label",{children:"Cung Mọc"}),u.jsx("span",{children:e.zodiac.rising})]})]}),u.jsxs("div",{className:"element-pill",children:["Nguyên tố: ",e.zodiac.element]}),u.jsx("style",{children:`
        .result-header-box {
          padding: 40px;
          border-radius: var(--radius-lg);
          border: 1px solid var(--white-10);
          background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
          position: relative;
          overflow: hidden;
          margin-bottom: 40px;
        }
        .element-fire { border-color: rgba(239, 68, 68, 0.3); background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), transparent); }
        .element-earth { border-color: rgba(22, 163, 74, 0.3); background: linear-gradient(135deg, rgba(22, 163, 74, 0.1), transparent); }
        .element-air { border-color: rgba(14, 165, 233, 0.3); background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), transparent); }
        .element-water { border-color: rgba(37, 99, 235, 0.3); background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), transparent); }

        .header-badge {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
        }
        .element-icon { font-size: 2rem; }
        .chart-type {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 2px;
          color: var(--white-40);
        }
        .header-title {
          font-size: 3rem;
          margin-bottom: 24px;
          color: white;
        }
        .zodiac-info-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 32px;
          margin-bottom: 24px;
        }
        .info-item label {
          display: block;
          font-size: 11px;
          color: var(--white-40);
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 4px;
        }
        .info-item span {
          font-size: 1.2rem;
          font-weight: 600;
          font-family: var(--font-display);
        }
        .element-pill {
          display: inline-block;
          padding: 6px 16px;
          background: var(--white-10);
          border-radius: 20px;
          font-size: 12px;
          font-weight: 600;
        }
      `})]})},Kg={Aries:"#ff4d4d",Taurus:"#4dff88",Gemini:"#ffff4d",Cancer:"#4db8ff",Leo:"#ff4d4d",Virgo:"#4dff88",Libra:"#ffff4d",Scorpio:"#4db8ff",Sagittarius:"#ff4d4d",Capricorn:"#4dff88",Aquarius:"#ffff4d",Pisces:"#4db8ff"},Qg=[{name:"Aries",element:"Fire"},{name:"Taurus",element:"Earth"},{name:"Gemini",element:"Air"},{name:"Cancer",element:"Water"},{name:"Leo",element:"Fire"},{name:"Virgo",element:"Earth"},{name:"Libra",element:"Air"},{name:"Scorpio",element:"Water"},{name:"Sagittarius",element:"Fire"},{name:"Capricorn",element:"Earth"},{name:"Aquarius",element:"Air"},{name:"Pisces",element:"Water"}],Gg={Fire:"#ff5f5f",Earth:"#82ca9d",Air:"#8884d8",Water:"#00d1ff"},qg=({planets:e})=>u.jsxs("div",{className:"chart-svg-container glass-card premium-chart",children:[u.jsxs("svg",{viewBox:"0 0 600 600",className:"natal-svg",children:[u.jsxs("defs",{children:[u.jsxs("filter",{id:"glow",x:"-20%",y:"-20%",width:"140%",height:"140%",children:[u.jsx("feGaussianBlur",{stdDeviation:"3",result:"blur"}),u.jsx("feComposite",{in:"SourceGraphic",in2:"blur",operator:"over"})]}),u.jsxs("radialGradient",{id:"ringGradient",children:[u.jsx("stop",{offset:"0%",stopColor:"rgba(255,255,255,0.05)"}),u.jsx("stop",{offset:"100%",stopColor:"transparent"})]})]}),u.jsx("circle",{cx:300,cy:300,r:270,fill:"none",stroke:"rgba(255,255,255,0.1)",strokeWidth:"1"}),u.jsx("circle",{cx:300,cy:300,r:228,fill:"none",stroke:"rgba(255,255,255,0.2)",strokeWidth:"2"}),Qg.map((s,a)=>{const c=a*30-180,f=(a+1)*30-180,d=(c+f)/2,h=300+270*Math.cos(c*Math.PI/180),w=300+270*Math.sin(c*Math.PI/180),m=300+270*Math.cos(f*Math.PI/180),v=300+270*Math.sin(f*Math.PI/180),k=300+246*Math.cos(d*Math.PI/180),g=300+246*Math.sin(d*Math.PI/180);return u.jsxs("g",{children:[u.jsx("path",{d:`M ${300+192*Math.cos(c*Math.PI/180)} ${300+192*Math.sin(c*Math.PI/180)} 
                   L ${h} ${w} A 270 270 0 0 1 ${m} ${v} 
                   L ${300+192*Math.cos(f*Math.PI/180)} ${300+192*Math.sin(f*Math.PI/180)} Z`,fill:a%2===0?"rgba(255,255,255,0.02)":"transparent",stroke:"rgba(255,255,255,0.05)",strokeWidth:"1"}),u.jsx("text",{x:k,y:g,className:"sign-text",fill:Gg[s.element],fontSize:"11",fontWeight:"700",textAnchor:"middle",alignmentBaseline:"middle",transform:`rotate(${d+90}, ${k}, ${g})`,children:s.name.toUpperCase()})]},a)}),e.slice(0,6).map((s,a)=>e.slice(a+1,8).map((c,f)=>{const d=s.longitude-180,h=c.longitude-180;return Math.abs(d-h)<30||Math.abs(d-h)>150?null:u.jsx("line",{x1:300+192*.8*Math.cos(d*Math.PI/180),y1:300+192*.8*Math.sin(d*Math.PI/180),x2:300+192*.8*Math.cos(h*Math.PI/180),y2:300+192*.8*Math.sin(h*Math.PI/180),stroke:"rgba(139, 92, 246, 0.15)",strokeWidth:"1"},`${a}-${f}`)})),e.map((s,a)=>{const c=s.longitude-180,f=300+150*Math.cos(c*Math.PI/180),d=300+150*Math.sin(c*Math.PI/180),h=300+192*.9*Math.cos(c*Math.PI/180),w=300+192*.9*Math.sin(c*Math.PI/180);return u.jsxs("g",{className:"planet-group",children:[u.jsx("line",{x1:f,y1:d,x2:h,y2:w,stroke:"rgba(255,255,255,0.2)",strokeWidth:"0.5"}),u.jsx("circle",{cx:f,cy:d,r:"4",fill:"var(--nebula-purple)",filter:"url(#glow)"}),u.jsx("text",{x:h,y:w,className:"planet-name-label",textAnchor:Math.cos(c*Math.PI/180)>0?"start":"end",alignmentBaseline:"middle",fontSize:"12",fill:"white",dx:Math.cos(c*Math.PI/180)>0?8:-8,children:s.name})]},a)}),u.jsx("circle",{cx:300,cy:300,r:150*.8,fill:"rgba(0,0,0,0.3)",stroke:"rgba(255,255,255,0.05)"}),u.jsx("path",{d:"M 280 300 L 320 300 M 300 280 L 300 320",stroke:"rgba(255,255,255,0.1)",strokeWidth:"1"})]}),u.jsx("style",{children:`
        .premium-chart {
          padding: 40px !important;
          max-width: 700px !important;
          margin-bottom: 60px !important;
          background: radial-gradient(circle at center, rgba(139, 92, 246, 0.05) 0%, transparent 70%);
        }
        .natal-svg {
          filter: drop-shadow(0 0 20px rgba(0,0,0,0.5));
        }
        .sign-text {
          font-family: var(--font-display);
          letter-spacing: 1px;
          opacity: 0.8;
        }
        .planet-name-label {
          font-family: var(--font-display);
          font-weight: 500;
          pointer-events: none;
        }
        .planet-group:hover circle {
          fill: var(--gold-primary);
          r: 6;
          transition: all 0.3s ease;
        }
      `})]}),Yg=({planets:e})=>u.jsxs("div",{className:"planet-list-container glass-card",children:[u.jsx("h2",{className:"section-card-title mb-4",children:"Vị trí các hành tinh"}),u.jsx("div",{className:"table-responsive",children:u.jsxs("table",{className:"planet-table",children:[u.jsx("thead",{children:u.jsxs("tr",{children:[u.jsx("th",{children:"Hành tinh"}),u.jsx("th",{children:"Cung"}),u.jsx("th",{children:"Kinh độ"})]})}),u.jsx("tbody",{children:e.map((t,n)=>u.jsxs("tr",{children:[u.jsx("td",{className:"planet-name",children:t.name}),u.jsx("td",{children:u.jsx("span",{className:"sign-badge",style:{color:Kg[t.sign]},children:t.sign})}),u.jsxs("td",{className:"longitude-val",children:[t.longitude.toFixed(2),"°"]})]},n))})]})}),u.jsx("style",{children:`
        .planet-list-container {
          margin-bottom: 40px;
          padding: 32px;
        }
        .planet-table {
          width: 100%;
          border-collapse: collapse;
        }
        .planet-table th {
          text-align: left;
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: 1px;
          color: var(--white-40);
          padding: 12px;
          border-bottom: 1px solid var(--white-10);
        }
        .planet-table td {
          padding: 12px;
          border-bottom: 1px solid var(--white-05);
        }
        .planet-name {
          font-weight: 600;
          color: var(--gold-primary);
        }
        .sign-badge {
          font-size: 13px;
          font-weight: 500;
        }
        .longitude-val {
          color: var(--white-40);
          font-size: 13px;
          font-family: monospace;
        }
      `})]}),Xg=e=>{const t=(e==null?void 0:e.details)||e;return{score:(t==null?void 0:t.score)||0,summary:(t==null?void 0:t.summary)||"Phân tích tương hợp",personality:(t==null?void 0:t.personality)||"Chưa có thông tin",love_style:(t==null?void 0:t.love_style)||"Chưa có thông tin",career:(t==null?void 0:t.career)||"Chưa có thông tin",relationships:(t==null?void 0:t.relationships)||"Chưa có thông tin",advice:(t==null?void 0:t.advice)||"Chưa có thông tin",conflict_points:(t==null?void 0:t.conflict_points)||"Chưa có thông tin",recommended_activities:(t==null?void 0:t.recommended_activities)||[],aspects:(t==null?void 0:t.aspects)||[],ai_analysis:t==null?void 0:t.ai_analysis,detailed_reasoning:t==null?void 0:t.detailed_reasoning}},Jg=[{name:"Mặt Trời",sign:"Libra",longitude:189.78},{name:"Mặt Trăng",sign:"Libra",longitude:203.5},{name:"Sao Thủy",sign:"Libra",longitude:181.3},{name:"Sao Kim",sign:"Scorpio",longitude:233.94},{name:"Sao Hỏa",sign:"Sagittarius",longitude:242.82},{name:"Sao Mộc",sign:"Aquarius",longitude:312.14},{name:"Sao Thổ",sign:"Aries",longitude:17.48},{name:"Thiên Vương",sign:"Aquarius",longitude:304.79},{name:"Hải Vương",sign:"Capricorn",longitude:297.19},{name:"Diêm Vương",sign:"Sagittarius",longitude:243.52},{name:"Nút Bắc",sign:"Virgo",longitude:168.49},{name:"Chiron",sign:"Scorpio",longitude:213.69}],Zg=()=>{const e=ae(l=>l.result),t=ae(l=>l.resultType),n=ae(l=>l.reset);if(!e)return null;if(t==="compatibility"||!e.sections||!Array.isArray(e.sections)){const l=typeof e=="string"?JSON.parse(e):e;console.log("🔍 Raw compatibility data in ResultPage:",JSON.stringify(l,null,2));const o=Xg(l),s=o.score||0,a=s>=50,c=o.summary,f=o.personality,d=o.love_style,h=o.career,w=o.relationships,m=o.advice,v=o.conflict_points,k=o.recommended_activities||[],g=o.aspects||[],p=o.ai_analysis,y=o.detailed_reasoning;return u.jsxs("div",{className:"container section-py",children:[u.jsx("button",{className:"btn-back",onClick:n,children:"← Quay lại"}),u.jsxs("div",{className:"compatibility-result-box",children:[u.jsxs("div",{className:"compatibility-header",children:[u.jsx("h1",{className:"title-gradient",children:"TƯƠNG HỢP HAI NGƯỜI"}),u.jsx("div",{className:"compatibility-score",children:u.jsxs("div",{className:"score-circle",children:[u.jsxs("span",{className:"score-number",children:[Math.round(s),"%"]}),u.jsx("span",{className:"score-label",children:"Độ hợp nhau"})]})})]}),u.jsxs("div",{className:"compatibility-result",children:[u.jsx("div",{className:`result-badge ${a?"compatible":"not-compatible"}`,children:a?"HỢP NHAU":"KHÔNG HỢP"}),u.jsxs("div",{className:"compatibility-summary",children:[u.jsx("h3",{children:"📊 Tổng Quan"}),u.jsx("p",{children:c})]}),u.jsxs("div",{className:"compatibility-sections",children:[u.jsxs("div",{className:"section-card",children:[u.jsx("h4",{children:"👥 Tính Cách"}),u.jsx("p",{children:f})]}),u.jsxs("div",{className:"section-card",children:[u.jsx("h4",{children:"💖 Phong Cách Yêu"}),u.jsx("p",{children:d})]}),u.jsxs("div",{className:"section-card",children:[u.jsx("h4",{children:"💼 Hợp Tác Công Việc"}),u.jsx("p",{children:h})]}),u.jsxs("div",{className:"section-card",children:[u.jsx("h4",{children:"🤝 Động Lực Mối Quan Hệ"}),u.jsx("p",{children:w})]})]}),u.jsxs("div",{className:"compatibility-details",children:[u.jsxs("div",{className:"detail-card",children:[u.jsx("h4",{children:"💡 Lời Khuyên"}),u.jsx("p",{children:m})]}),u.jsxs("div",{className:"detail-card",children:[u.jsx("h4",{children:"⚠️ Điểm Xung Đột"}),u.jsx("p",{children:v})]})]}),k.length>0&&u.jsxs("div",{className:"activities-section",children:[u.jsx("h4",{children:"🎯 Hoạt Động Khuyến Nghị"}),u.jsx("ul",{children:k.map((S,N)=>u.jsx("li",{children:S},N))})]}),g.length>0&&u.jsxs("div",{className:"aspects-section",children:[u.jsx("h4",{children:"🌟 Các Mặt Trời"}),u.jsx("div",{className:"aspects-list",children:g.map((S,N)=>u.jsx("div",{className:"aspect-item",children:S},N))})]}),p&&u.jsxs("div",{className:"ai-analysis-box",children:[u.jsx("h3",{children:"🤖 Phân tích AI Tối Ưu"}),u.jsx("div",{className:"ai-analysis-content",children:p.split(`
`).map((S,N)=>u.jsx("p",{className:"ai-analysis-line",children:S},N))})]}),y&&u.jsxs("div",{className:"detailed-reasoning-box",children:[u.jsx("h3",{children:"🔍 Lý Do Chi Tiết"}),u.jsx("div",{className:"reasoning-content",children:y.split(`
`).map((S,N)=>u.jsx("p",{className:"reasoning-line",children:S},N))})]})]})]}),u.jsx("style",{children:`
          .compatibility-result-box {
            background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            border: 1px solid var(--white-10);
            border-radius: var(--radius-lg);
            padding: 40px;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
          }
          
          .compatibility-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 20px;
          }
          
          .title-gradient {
            font-size: 2.5rem;
            margin: 0;
            background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }
          
          .compatibility-score {
            display: flex;
            justify-content: center;
            align-items: center;
          }
          
          .score-circle {
            width: 120px;
            height: 120px;
            border: 4px solid var(--white-20);
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
          }
          
          .score-circle::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border: 4px solid transparent;
            border-top-color: var(--nebula-purple);
            border-radius: 50%;
            animation: rotate 2s linear infinite;
            opacity: 0.5;
          }
          
          .score-number {
            font-size: 2rem;
            font-weight: 800;
            color: white;
            z-index: 1;
          }
          
          .score-label {
            font-size: 0.8rem;
            color: var(--white-40);
            text-transform: uppercase;
            z-index: 1;
          }
          
          .compatibility-result {
            display: flex;
            flex-direction: column;
            gap: 24px;
          }
          
          .result-badge {
            font-size: 1.5rem;
            font-weight: 800;
            padding: 12px 24px;
            border-radius: 30px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
            border: 2px solid var(--white-20);
          }
          
          .compatible {
            background: rgba(34, 197, 94, 0.1);
            color: #22c55e;
            border-color: #22c55e;
          }
          
          .not-compatible {
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            border-color: #ef4444;
          }
          
          .compatibility-summary {
            background: rgba(255,255,255,0.02);
            padding: 20px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--nebula-purple);
          }
          
          .compatibility-summary h3 {
            margin: 0 0 10px 0;
            color: var(--white-70);
            font-size: 1.1rem;
          }
          
          .compatibility-summary p {
            margin: 0;
            color: var(--white-40);
            line-height: 1.6;
          }

          .compatibility-sections {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
          }

          .section-card {
            background: rgba(255,255,255,0.02);
            padding: 16px;
            border-radius: var(--radius-md);
            border: 1px solid var(--white-10);
          }

          .section-card h4 {
            margin: 0 0 8px 0;
            color: var(--nebula-purple);
            font-size: 1rem;
          }

          .section-card p {
            margin: 0;
            color: var(--white-40);
            line-height: 1.6;
            font-size: 0.9rem;
          }

          .compatibility-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
          }

          .detail-card {
            background: rgba(255,255,255,0.02);
            padding: 16px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--nebula-blue);
          }

          .detail-card h4 {
            margin: 0 0 8px 0;
            color: var(--nebula-blue);
            font-size: 1rem;
          }

          .detail-card p {
            margin: 0;
            color: var(--white-40);
            line-height: 1.6;
            font-size: 0.9rem;
          }

          .activities-section {
            background: rgba(255,255,255,0.02);
            padding: 16px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--gold-primary);
          }

          .activities-section h4 {
            margin: 0 0 12px 0;
            color: var(--gold-primary);
            font-size: 1rem;
          }

          .activities-section ul {
            margin: 0;
            padding-left: 20px;
            color: var(--white-40);
            line-height: 1.6;
            font-size: 0.9rem;
          }

          .activities-section li {
            margin-bottom: 4px;
          }

          .aspects-section {
            background: rgba(255,255,255,0.02);
            padding: 16px;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--nebula-pink);
          }

          .aspects-section h4 {
            margin: 0 0 12px 0;
            color: var(--nebula-pink);
            font-size: 1rem;
          }

          .aspects-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 8px;
          }

          .aspect-item {
            background: rgba(255,255,255,0.02);
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            border: 1px solid rgba(255,255,255,0.1);
            color: var(--white-40);
            font-size: 0.9rem;
          }

          @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          
          @media (max-width: 768px) {
            .compatibility-header {
              flex-direction: column;
              align-items: flex-start;
            }
            .score-circle {
              width: 100px;
              height: 100px;
            }
            .score-number {
              font-size: 1.5rem;
            }
            .compatibility-sections {
              grid-template-columns: 1fr;
            }
            .compatibility-details {
              grid-template-columns: 1fr;
            }
          }

          .ai-analysis-box {
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: var(--radius-md);
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid var(--nebula-purple);
          }

          .ai-analysis-box h3 {
            margin: 0 0 12px 0;
            color: var(--nebula-purple);
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 8px;
          }

          .ai-analysis-content {
            background: rgba(255, 255, 255, 0.02);
            padding: 16px;
            border-radius: var(--radius-sm);
            border: 1px solid rgba(255, 255, 255, 0.1);
          }

          .ai-analysis-line {
            margin: 8px 0;
            color: var(--white-40);
            line-height: 1.6;
            font-style: italic;
          }

          .detailed-reasoning-box {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: var(--radius-md);
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid var(--nebula-blue);
          }

          .detailed-reasoning-box h3 {
            margin: 0 0 12px 0;
            color: var(--nebula-blue);
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 8px;
          }

          .reasoning-content {
            background: rgba(255, 255, 255, 0.02);
            padding: 16px;
            border-radius: var(--radius-sm);
            border: 1px solid rgba(255, 255, 255, 0.1);
          }

          .reasoning-line {
            margin: 8px 0;
            color: var(--white-40);
            line-height: 1.6;
          }
        `})]})}if(t==="zodiac_ai"&&e.report){const l=e;return u.jsxs("div",{className:"container section-py",children:[u.jsx("button",{className:"btn-back",onClick:n,children:"← TRỞ VỀ TRANG CHỦ"}),u.jsx(Vg,{report:l.report,chartData:l.chart_data,generatedAt:l.generated_at,placements:l.placements})]})}if(t==="standard"&&e.report){const l=e;return u.jsxs("div",{className:"container section-py",children:[u.jsx("button",{className:"btn-back",onClick:n,children:"← TRỞ VỀ TRANG CHỦ"}),u.jsx(Hg,{report:l.report,chartData:l.chart_data,generatedAt:l.generated_at})]})}const r=e,i=r.meta.planets||Jg;return u.jsxs("div",{className:"container section-py",children:[u.jsx("button",{className:"btn-back",onClick:n,children:"← TRỞ VỀ TRANG CHỦ"}),u.jsx(Wg,{meta:r.meta}),u.jsxs("div",{className:"chart-grid",children:[u.jsx(qg,{planets:i}),u.jsx(Yg,{planets:i})]}),u.jsx("div",{className:"result-footer",children:u.jsxs("p",{children:["Phân tích dựa trên"," ",r.meta.chartType==="with_birth_time"?"thông tin đầy đủ":"thông tin cơ bản",". Kết quả mang tính tham khảo và phản ánh xu hướng năng lượng chiêm tinh."]})}),u.jsx("style",{children:`
        .btn-back {
          background: none;
          border: none;
          color: var(--white-40);
          cursor: pointer;
          margin-bottom: 40px;
          letter-spacing: 2px;
          font-weight: 700;
          font-family: var(--font-display);
          transition: color 0.3s;
        }
        .btn-back:hover { color: var(--nebula-pink); }
        .chart-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 30px;
          margin-bottom: 40px;
        }
        @media (max-width: 992px) {
          .chart-grid { grid-template-columns: 1fr; }
        }
        .sections-container {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .result-footer {
          margin-top: 60px;
          text-align: center;
          padding: 40px;
          border-top: 1px solid var(--white-10);
        }
        .result-footer p {
          color: var(--white-40);
          font-size: 13px;
          max-width: 600px;
          margin: 0 auto;
        }
      `})]})};function e0(){const e=ae(t=>t.result);return u.jsxs(u.Fragment,{children:[u.jsx("div",{className:"stars-overlay"}),u.jsx("div",{className:"app-container",children:e?u.jsx(Zg,{}):u.jsx($g,{})})]})}const du=document.getElementById("root");du&&zl.createRoot(du).render(u.jsx(Eu.StrictMode,{children:u.jsx(e0,{})}));
