webpackJsonp([2],[,,,,,,,,,,function(t,e,s){"use strict";var a=s(2),i=s(56),n=s(48),o=s.n(n),r=s(49),c=s.n(r),l=s(50),u=s.n(l);a.a.use(i.a);var v={path:"/",name:"LandingPage",component:o.a},d={path:"/session/:id",name:"Session",component:c.a,props:!0},f={path:"/sessions",name:"Sessions",component:u.a};e.a=new i.a({routes:[v,d,f]})},function(t,e,s){"use strict";var a=s(2),i=s(4),n=s(37);a.a.use(i.a),e.a=new i.a.Store({state:{session:{},sessions:[],monitorStatus:{status:!1,connected:!1,streaming:!1,message:"Board Not Detected"},socket:{}},mutations:{setSocket:function(t){t.socket=io.connect("http://localhost:5200")},setStatus:function(t,e){t.monitorStatus=e},setSession:function(t,e){t.session=e},setSessions:function(t,e){t.sessions=e}},actions:{establishSocketConnection:function(t){t.commit("setSocket"),t.state.socket.emit("request_status")},createSession:function(t){n.a.postResource("sessions",{}).then(function(e){t.commit("setSession",e.data),router.push({name:"Session",params:{id:e.data._id}})})},getSession:function(t,e){n.a.getResource("session",e).then(function(e){t.commit("setSession",e.data)})},getSessions:function(t){n.a.listResource("sessions").then(function(e){t.commit("setSessions",e.data)})}}})},function(t,e,s){function a(t){s(44)}var i=s(1)(s(32),s(55),a,"data-v-9143a9b2",null);t.exports=i.exports},,,,,,,,,,,,,,,,,,,,function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={name:"app",data:function(){return{clipped:!0,drawer:!0,fixed:!0,items:[{icon:"add_circle",text:"Add Session",route:"LandingPage"},{icon:"archive",text:"Sessions Archive",route:"Sessions"},{icon:"settings",text:"Settings",route:"LandingPage"},{icon:"help",text:"Help",route:"LandingPage"}],miniVariant:!1,right:!0,rightDrawer:!1,title:"new vital signs"}},computed:{monitorStatus:function(){return this.$store.state.monitorStatus}},methods:{setStatus:function(t){this.$store.commit("setStatus",t)}},mounted:function(){console.log("App Mounted"),this.$store.dispatch("establishSocketConnection"),this.$store.state.socket.on("status",this.setStatus)}}},function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={components:{},props:{},data:function(){return{autoScaleTime:0,autoScaleInterval:500,stdAbove:600,stdBelow:200,openConfig:!1,intervalId:null,chart:null,sampleBuffer:[],timeBuffer:[],samplingRate:0,timeSeries:null,topScale:7500,botScale:0,speedScale:4,weightedMean:0,weightedVar:0,scaleSensitivity:200,autoScale:!1,autoScaleIterations:0,boardTime:0,leaveTime:0,maxTime:0,plotFiltered:!0}},methods:{resize:function(){var t=$("#data").width();$("#chart").attr("width",t)},updateBuffer:function(t){console.log("Data Available.");var e=(new Date).getTime(),s=t[1];if(s&&(this.timeSeries.append((new Date).getTime(),s),this.autoScale)){this.weightedMean=(1-this.alphaDecay)*this.weightedMean+this.alphaDecay*s,this.weightedVar=(1-this.alphaDecay)*(this.weightedVar+this.alphaDecay*Math.pow(s-this.weightedMean,2));var a=Math.sqrt(this.weightedVar),i=this.weightedMean-this.stdBelow/100*a,n=this.weightedMean+this.stdAbove/100*a;e-this.autoScaleTime>this.autoScaleInterval&&(this.topScale=1e4*n,this.botScale=1e4*i,this.autoScaleTime=(new Date).getTime())}}},watch:{topScale:function(){this.chart.options.maxValue=this.topScale/1e4},botScale:function(){this.chart.options.minValue=this.botScale/1e4},speedScale:function(){this.chart.options.millisPerPixel=this.speedScale}},computed:{alphaDecay:function(){return Math.pow(10,-this.scaleSensitivity/100)}},mounted:function(){var t={};t.interpolation="linear",t.scaleSmoothing=.04,t.maxValue=2.5,t.minValue=0,this.topScale=2500,this.botScale=0,t.millisPerPixel=this.speedScale,t.grid={linewidth:1,verticalSections:4,fillStyle:"#fefefe"},t.labels={fillStyle:"#000000",fontSize:18},this.chart=new SmoothieChart(t),this.chart.streamTo(document.getElementById("chart"),1e3),$(window).resize(function(){var t=$("#data").width();$("#chart").attr("width",t)}),setTimeout(this.resize,500);var e={};e.strokeStyle="#c62828",e.lineWidth=3,e.fillStyle="rgba(0,0,35,0.1)",e.opacity=.2,this.timeSeries=new TimeSeries,this.chart.addTimeSeries(this.timeSeries,e),this.$store.dispatch("establishSocketConnection"),this.$store.state.socket.on("data_package",this.updateBuffer)}}},function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={components:{},props:[],data:function(){return{sessionId:""}},methods:{keyPress:function(){},focusInput:function(){this.sessionId=null},openSession:function(){},createSession:function(){this.$store.dispatch("createSession")}},computed:{},mounted:function(){}}},function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=s(47),i=s.n(a);e.default={components:{Chart:i.a},props:["id"],data:function(){return{isRecording:!1}},methods:{updateRate:function(t){this.samplingRate=t},toggleRecord:function(){this.isRecording?this.$store.state.socket.emit("stop_record"):this.$store.state.socket.emit("start_record",this.session._id),this.isRecording=!this.isRecording}},computed:{session:function(){return this.$store.state.session}},mounted:function(){console.log("Mounted!"),this.$store.dispatch("getSession",this.id)}}},function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={components:{},props:[],data:function(){return{search:"",headers:[{text:"Code",value:"hid",sortable:!1,align:"left"},{text:"Created At",value:"createdAt",sortable:!0,align:"left"}],pagination:{sortBy:"createdAt"}}},methods:{visitSession:function(t){this.$router.push({name:"Session",params:{id:t._id}})}},computed:{sessions:function(){return this.pagination.descending=!0,this.$store.state.sessions}},mounted:function(){this.$store.dispatch("getSessions")}}},function(t,e,s){"use strict";var a=s(14),i=s.n(a);window.axios=i.a;var n="http://localhost:5100";e.a={getStatic:function(t){var e=n+"/"+t;return i.a.get(e)},queryResource:function(t,e,s){var a=n+"/"+t+"?"+e+"="+s;return i.a.get(a)},getResource:function(t,e){var s=n+"/"+t+"/"+e;return i.a.get(s)},listResource:function(t){var e=n+"/"+t;return i.a.get(e)},deleteResource:function(t,e){var s=n+"/"+t+"/"+e;return i.a.delete(s)},postResource:function(t,e){var s=n+"/"+t;return i.a.post(s,e)},postNestedResource:function(t,e,s,a){var o=n+"/"+t+"/"+e+"/"+s;return i.a.post(o,a)},listNestedResource:function(t,e,s){var a=n+"/"+t+"/"+e+"/"+s;return i.a.get(a)},putResource:function(t,e){var s=n+"/"+t+"/"+e._id;return i.a.put(s,e)},streamResource:function(t,e){var s=n+"/"+t+"/"+e.id;return s+="/stream",s+="?elapsedTime="+e.elapsedTime,i.a.get(s,e)},getHistory:function(t,e){var s=n+"/"+t+"/"+e.id;return s+="/history",i.a.get(s,e)}}},function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=s(2),i=s(13),n=s.n(i),o=s(12),r=s.n(o),c=s(10),l=s(4),u=s(11);s.e(0).then(s.bind(null,39)),a.a.config.productionTip=!1,a.a.use(l.a),a.a.use(n.a);var v=new a.a({el:"#app",router:c.a,store:u.a,template:"<App/>",components:{App:r.a}});window.router=v.$router,a.a.filter("formatNumber",function(t,e){return sprintf(e,t)})},,function(t,e){},function(t,e){},function(t,e){},function(t,e){},function(t,e){},,,function(t,e,s){function a(t){s(42)}var i=s(1)(s(33),s(53),a,"data-v-8cc91162",null);t.exports=i.exports},function(t,e,s){function a(t){s(43)}var i=s(1)(s(34),s(54),a,"data-v-8d585c12",null);t.exports=i.exports},function(t,e,s){function a(t){s(40)}var i=s(1)(s(35),s(51),a,"data-v-2f3073c7",null);t.exports=i.exports},function(t,e,s){function a(t){s(41)}var i=s(1)(s(36),s(52),a,"data-v-8aecb388",null);t.exports=i.exports},function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("v-container",{attrs:{fluid:""}},[s("v-card",[s("v-card-title",[s("span",{staticClass:"human-id"},[t._v(t._s(t.session.hid))]),t._v(" "),s("v-spacer"),t._v(" "),t.isRecording?s("v-btn",{staticClass:"white--text",attrs:{primary:"",large:""},nativeOn:{click:function(e){t.toggleRecord(e)}}},[s("v-icon",{staticClass:"white--text",attrs:{left:""}},[t._v("pause")]),t._v("\n        Pause\n      ")],1):s("v-btn",{staticClass:"white--text primary",attrs:{primary:"",large:""},nativeOn:{click:function(e){t.toggleRecord(e)}}},[s("v-icon",{staticClass:"white--text",attrs:{left:""}},[t._v("fiber_manual_record")]),t._v("\n        Record\n      ")],1)],1)],1),t._v(" "),s("br"),t._v(" "),s("v-card",[s("v-card-text",[s("chart")],1)],1)],1)},staticRenderFns:[]}},function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("v-container",[s("v-card",[s("v-card-title",[s("v-subheader",[t._v("\n        Sessions\n      ")])],1)],1),t._v(" "),s("br"),t._v(" "),s("v-card",[s("v-card-text",[s("v-data-table",{attrs:{pagination:t.pagination,search:t.search,headers:t.headers,"no-data-text":"No Sessions Available",items:t.sessions},on:{"update:pagination":function(e){t.pagination=e}},scopedSlots:t._u([{key:"items",fn:function(e){return[s("tr",{on:{click:function(s){t.visitSession(e.item)}}},[s("td",[s("h5",[t._v(t._s(e.item.hid))])]),t._v(" "),s("td",[t._v(t._s(e.item.createdAt))])])]}}])})],1)],1)],1)},staticRenderFns:[]}},function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("v-layout",[s("v-flex",{attrs:{xs5:""}},[s("v-layout",[s("v-flex",[s("v-slider",{attrs:{disabled:t.autoScale,label:"Max",max:"25000",min:"0"},model:{value:t.topScale,callback:function(e){t.topScale=e},expression:"topScale"}})],1)],1),t._v(" "),s("v-layout",[s("v-flex",[s("v-slider",{attrs:{disabled:t.autoScale,label:"MIN",max:"25000",min:"0"},model:{value:t.botScale,callback:function(e){t.botScale=e},expression:"botScale"}})],1)],1),t._v(" "),s("v-layout",[s("v-flex",[s("v-slider",{attrs:{label:"TIME",max:"20",min:"0"},model:{value:t.speedScale,callback:function(e){t.speedScale=e},expression:"speedScale"}})],1)],1),t._v(" "),s("v-layout",[s("v-flex",{attrs:{xs7:""}},[s("v-checkbox",{attrs:{color:"primary",label:"Autoscale"},model:{value:t.autoScale,callback:function(e){t.autoScale=e},expression:"autoScale"}})],1),t._v(" "),s("v-flex",{attrs:{xs4:""}},[s("v-btn",{staticClass:"mt-3",attrs:{icon:""},nativeOn:{click:function(e){t.openConfig=!0}}},[s("v-icon",[t._v("settings")])],1)],1)],1)],1),t._v(" "),s("v-flex",{attrs:{xs12:"",id:"data"}},[s("canvas",{attrs:{id:"chart",height:"275"}})]),t._v(" "),s("v-dialog",{attrs:{width:"500px",persistent:""},model:{value:t.openConfig,callback:function(e){t.openConfig=e},expression:"openConfig"}},[s("v-card",[s("v-card-title",[s("v-subheader",[t._v("\n      AutoScale Options\n      ")])],1),t._v(" "),s("v-divider"),t._v(" "),s("v-card-text",[s("v-layout",[s("v-flex",{staticClass:"input-group",attrs:{xs4:""}},[s("label",[t._v("Smoothing")])]),t._v(" "),s("v-flex",{attrs:{xs6:""}},[s("v-slider",{attrs:{max:"300",min:"0",step:"1"},model:{value:t.scaleSensitivity,callback:function(e){t.scaleSensitivity=e},expression:"scaleSensitivity"}})],1),t._v(" "),s("v-flex",{staticClass:"mt-3",attrs:{xs2:""}},[t._v("\n          "+t._s(t._f("formatNumber")(t.alphaDecay,"%0.3f"))+"\n        ")])],1),t._v(" "),s("v-layout",[s("v-flex",{staticClass:"input-group",attrs:{xs4:""}},[s("label",[t._v("Deviations Above")])]),t._v(" "),s("v-flex",{attrs:{xs6:""}},[s("v-slider",{attrs:{max:"1000",min:"10",step:"1"},model:{value:t.stdAbove,callback:function(e){t.stdAbove=e},expression:"stdAbove"}})],1),t._v(" "),s("v-flex",{staticClass:"mt-3",attrs:{xs2:""}},[t._v("\n          "+t._s(t._f("formatNumber")(t.stdAbove/100,"%0.2f"))+"\n        ")])],1),t._v(" "),s("v-layout",[s("v-flex",{staticClass:"input-group",attrs:{xs4:""}},[s("label",[t._v("Deviations Below")])]),t._v(" "),s("v-flex",{attrs:{xs6:""}},[s("v-slider",{attrs:{max:"1000",min:"10",step:"1"},model:{value:t.stdBelow,callback:function(e){t.stdBelow=e},expression:"stdBelow"}})],1),t._v(" "),s("v-flex",{staticClass:"mt-3",attrs:{xs2:""}},[t._v("\n          "+t._s(t._f("formatNumber")(t.stdBelow/100,"%0.2f"))+"\n        ")])],1)],1),t._v(" "),s("v-card-actions",[s("v-spacer"),t._v(" "),s("v-btn",{attrs:{flat:"",primary:""},nativeOn:{click:function(e){t.openConfig=!1}}},[t._v("\n        Close\n      ")])],1),t._v("j\n  ")],1)],1)],1)},staticRenderFns:[]}},function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("v-container",[s("v-layout",{staticClass:"form",attrs:{"align-center":"","justify-center":""}},[s("h1",{staticClass:"logo text--white"},[t._v("NEW VITAL SIGNS")])]),t._v(" "),s("v-layout",{attrs:{"align-center":"","justify-center":""}},[s("v-btn",{staticClass:"large-btn white--text",attrs:{large:""},nativeOn:{click:function(e){t.createSession(e)}}},[t._v("\n        Create New Session\n      ")])],1)],1)},staticRenderFns:[]}},function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("v-app",{attrs:{light:""}},[s("v-toolbar",{attrs:{fixed:""}},[s("v-btn",{staticClass:"menu-btn",attrs:{icon:""},nativeOn:{click:function(e){e.stopPropagation(),t.rightDrawer=!t.rightDrawer}}},[s("v-icon",{staticClass:"menu-btn"},[t._v("menu")])],1),t._v(" "),s("a",{attrs:{href:"/#"}},[s("img",{staticClass:"nvs-logo",attrs:{src:"static/img/favicon@2x.png"}})]),t._v(" "),s("v-toolbar-title",{staticClass:"title-logo",domProps:{textContent:t._s(t.title)}}),t._v(" "),s("v-spacer"),t._v(" "),t.monitorStatus.connected?s("v-chip",{staticClass:"success white--text",attrs:{label:""}},[s("v-icon",{staticClass:"white--text",staticStyle:{opacity:"1"},attrs:{left:""}},[t._v("\n        swap_vert\n      ")]),t._v("\n      "+t._s(t.monitorStatus.message)+"\n    ")],1):s("v-chip",{staticClass:"error white--text",attrs:{label:""}},[s("v-icon",{staticClass:"white-text",staticStyle:{opacity:"1"},attrs:{left:""}},[t._v("\n        warning\n      ")]),t._v("\n      "+t._s(t.monitorStatus.message)+"\n    ")],1)],1),t._v(" "),s("v-navigation-drawer",{attrs:{temporary:"",clipped:t.clipped,right:!1},model:{value:t.rightDrawer,callback:function(e){t.rightDrawer=e},expression:"rightDrawer"}},[s("v-list",{attrs:{dense:""}},[t._l(t.items,function(e,a){return[e.heading?s("v-layout",{key:a,attrs:{row:"","align-left":""}},[s("v-flex",{attrs:{xs12:""}},[e.heading?s("v-subheader",[t._v("\n              "+t._s(e.heading)+"\n            ")]):t._e()],1)],1):e.divider?s("v-divider",{key:a,staticClass:"my-4 black--text",attrs:{light:""}}):s("v-list-tile",{key:a,attrs:{to:{name:e.route}}},[s("v-list-tile-action",[s("v-icon",{staticClass:"side-icon"},[t._v(t._s(e.icon))])],1),t._v(" "),s("v-list-tile-content",[s("v-list-tile-title",[t._v("\n              "+t._s(e.text)+"\n            ")])],1)],1)]})],2)],1),t._v(" "),s("main",[s("router-view")],1)],1)},staticRenderFns:[]}}],[38]);
//# sourceMappingURL=app.d41c10161585c508dc31.js.map