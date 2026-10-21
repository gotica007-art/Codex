'use strict';
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),{randomBytes}=require('node:crypto');
const AI=require('./ai');
const ROOT=__dirname,MAX_VIDEO=24*1024*1024;
function config(directory=ROOT,env=process.env){
 const filename=path.join(directory,'config.local.json');let local={};
 try{local=JSON.parse(fs.readFileSync(filename,'utf8').replace(/^\uFEFF/,''));}
 catch(e){if(e.code!=='ENOENT')throw Error('config.local.json tiene un formato JSON inválido. Revisa comillas y comas; no compartas su contenido.');
  if(fs.existsSync(filename+'.txt'))throw Error('El archivo se llama config.local.json.txt. Activa las extensiones de Windows y quita .txt.');
 }
 if(!local||typeof local!=='object'||Array.isArray(local))throw Error('config.local.json debe contener un objeto JSON.');
 const value=(name,fallback='')=>{const v=env[name]||local[name]||fallback;if(typeof v!=='string')throw Error('Los valores de configuración deben estar entre comillas.');return v.trim();};
 const key=value('OPENAI_API_KEY');
 return {key,model:value('OPENAI_TEXT_MODEL','gpt-4.1-mini'),transcribe:value('OPENAI_TRANSCRIBE_MODEL','gpt-transcribe'),configPath:filename,keySource:env.OPENAI_API_KEY?.trim()?'variable de entorno OPENAI_API_KEY':key?'config.local.json':'sin clave'};
}
async function openai(endpoint,body,isJson=true,settings=config(),fetcher=fetch){
 if(!settings.key)throw Error('Falta la clave de OpenAI. Guarda config.local.json y pulsa Comprobar configuración. Puedes seguir editando manualmente.');
 let r;try{r=await fetcher('https://api.openai.com/v1/'+endpoint,{method:'POST',headers:{Authorization:'Bearer '+settings.key,...(isJson?{'Content-Type':'application/json'}:{})},body:isJson?JSON.stringify(body):body,signal:AbortSignal.timeout(180000)});}catch{throw Error('No se pudo contactar con OpenAI o se agotó el tiempo. Comprueba tu conexión. No se reintenta automáticamente; una solicitud podría haberse facturado.');}
 if(!r.ok){const messages={401:'La clave de OpenAI no es válida.',403:'La cuenta no tiene permiso para usar este servicio.',404:'El modelo configurado no está disponible. Revisa su nombre en config.local.json.',429:'OpenAI ha rechazado la solicitud por cuota, saldo o límite de uso.',413:'El archivo supera el límite del servicio.',400:'OpenAI no pudo procesar el archivo o la solicitud. Comprueba formato, audio y modelo.'};throw Error(messages[r.status]||'El servicio de IA no pudo completar la solicitud. Inténtalo más tarde.');}
 try{return await r.json();}catch{throw Error('El servicio de IA devolvió una respuesta ilegible.');}
}
async function generate(d,settings=config(),fetcher=fetch){const body=AI.requestBody(d,settings.model);const result=await openai('responses',body,true,settings,fetcher);if(result.status&&result.status!=='completed')throw Error('La IA no completó la propuesta. No se añadieron preguntas.');const parts=(result.output||[]).filter(x=>x.type==='message').flatMap(x=>x.content||[]);if(parts.some(x=>x.type==='refusal'))throw Error('El servicio no pudo generar preguntas sobre este contenido.');let data;try{data=JSON.parse(parts.filter(x=>x.type==='output_text').map(x=>x.text).join(''));}catch{throw Error('La IA no devolvió una propuesta válida. No se añadieron preguntas.');}return AI.validateProposal(data,d);}
async function transcribe(bytes,filename,settings=config(),fetcher=fetch){const ext=path.extname(filename).toLowerCase();if(!['.mp4','.webm','.mp3','.m4a','.wav'].includes(ext)||!bytes.length||bytes.length>MAX_VIDEO)throw Error('Usa MP4, WebM, MP3, M4A o WAV, con audio y hasta 24 MB. También puedes pegar la transcripción.');const data=new FormData();data.append('model',settings.transcribe);data.append('file',new Blob([bytes]),'fuente'+ext);data.append('response_format','json');const result=await openai('audio/transcriptions',data,false,settings,fetcher);if(typeof result.text!=='string'||result.text.trim().length<100||result.text.length>AI.MAX_TRANSCRIPT)throw Error('No se obtuvo una transcripción utilizable de 100 a 60000 caracteres. Revisa el audio o pega la transcripción manualmente.');return {transcript:result.text};}
function createServer(settingsProvider=config,fetcher=fetch){let busy=false;const token=randomBytes(24).toString('hex');
 return http.createServer(async(req,res)=>{const send=(status,data)=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(data));};
 const expected='127.0.0.1:'+req.socket.localPort;
 if(req.headers.host!==expected)return send(403,{error:'Dirección local no válida. Abre la aplicación desde INICIAR-IA.cmd.'});
 if(req.headers.origin&&req.headers.origin!=='http://'+expected)return send(403,{error:'Origen no autorizado.'});
 const url=new URL(req.url,'http://'+expected),route=url.pathname;
 let settings,configError;
 if(route.startsWith('/api/')){try{settings=typeof settingsProvider==='function'?settingsProvider():settingsProvider;}catch(e){configError=e.message;}}
 if(req.method==='GET'&&route==='/api/status')return send(200,{configured:!!settings?.key,model:settings?.model,transcribeModel:settings?.transcribe,configPath:settings?.configPath||path.join(ROOT,'config.local.json'),keySource:settings?.keySource,error:configError,token});
 if(req.method==='GET'){const files={'/':'index.html','/index.html':'index.html','/core.js':'core.js','/app.js':'app.js','/styles.css':'styles.css'};if(!files[route])return send(404,{error:'Archivo no disponible.'});const file=files[route],ext=path.extname(file);res.writeHead(200,{'Content-Type':({'.html':'text/html','.js':'text/javascript','.css':'text/css'}[ext])+'; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'self'; frame-src https://www.youtube-nocookie.com; connect-src 'self'; img-src 'self' data:; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"});return res.end(fs.readFileSync(path.join(ROOT,file)));}
 if(req.method!=='POST'||!['/api/generate','/api/transcribe'].includes(route))return send(404,{error:'Ruta no disponible.'});
 if(req.headers['x-session-token']!==token)return send(403,{error:'Sesión no válida. Recarga la aplicación.'});
 if(busy)return send(429,{error:'Ya hay una solicitud en curso. Espera a que termine.'});
 if(configError)return send(503,{error:configError});
 if(!settings.key)return send(503,{error:'Falta configurar la clave de OpenAI en config.local.json. No la pegues en la página ni en el chat.'});
 const isGenerate=route==='/api/generate',limit=isGenerate?300000:MAX_VIDEO;
 if(isGenerate&&!String(req.headers['content-type']).startsWith('application/json'))return send(415,{error:'Se requiere JSON.'});
 const length=Number(req.headers['content-length']);if(!Number.isFinite(length)||length<1||length>limit)return send(413,{error:'Solicitud vacía o demasiado grande. Máximo 24 MB por video.'});
 busy=true;try{let size=0,chunks=[];for await(const chunk of req){size+=chunk.length;if(size>limit)throw Error('El archivo supera el máximo permitido.');chunks.push(chunk);}const bytes=Buffer.concat(chunks);let result;if(isGenerate){let d;try{d=JSON.parse(bytes);}catch{throw Error('La solicitud JSON no es válida.');}result=await generate(d,settings,fetcher);}else result=await transcribe(bytes,String(req.headers['x-file-name']||'video.mp4'),settings,fetcher);send(200,result);}catch(e){send(400,{error:e.message});}finally{busy=false;}
 });}
if(require.main===module){try{const port=Number(process.env.PORT||8765);if(!Number.isInteger(port)||port<1024||port>65535)throw Error('Puerto inválido.');const server=createServer();server.on('error',()=>{console.error('No se pudo iniciar. Cierra otra instancia o usa otro puerto PORT.');process.exitCode=1;});server.listen(port,'127.0.0.1',()=>console.log('Abre http://127.0.0.1:'+port+' en Edge o Chrome. Mantén esta ventana abierta.'));}catch(e){console.error(e.message);process.exitCode=1;}}
module.exports={createServer,generate,transcribe,openai,config};
