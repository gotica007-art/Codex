"""Prueba de interfaz con respuestas IA simuladas, sin llamadas externas ni cargos."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import functools,http.server,threading,json
BASE=Path(__file__).resolve().parents[1]
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(BASE)))
threading.Thread(target=server.serve_forever,daemon=True).start()
source='El agua líquida se transforma en vapor cuando recibe calor. La evaporación ocurre en la superficie del agua. Al enfriarse, el vapor se condensa en gotas de agua líquida.'
objectives=[{'id':'O1','text':'Identificar la evaporación del agua'}]
def question(id,type,title,options,correct):
 return dict(id=id,type=type,title=title,text='',example='',video='',options=options,correct=correct,feedbackCorrect='El calor transforma el agua líquida en vapor.',feedbackIncorrect='La respuesta correcta se refiere al vapor: el agua cambia de estado, no desaparece.',evidence='El agua líquida se transforma en vapor cuando recibe calor.',objectiveIds=['O1'],reviewed=False)
proposal={'objectives':objectives,'questions':[question('q1','multiple','¿En qué se transforma el agua al recibir calor?',['Vapor','Metal','Piedra','Nada'],0),question('q2','boolean','El agua puede pasar a vapor.',['','','',''],0)]}
requests=[]
def generate(route):
 d=route.request.post_data_json;requests.append(d)
 if 'SIN CONTENIDO' in d['transcript']:route.fulfill(status=400,json={'error':'Fuente insuficiente para generar preguntas.'})
 else:route.fulfill(json=proposal)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1280,'height':1000},accept_downloads=True)
 errors=[];alerts=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('dialog',lambda d:(alerts.append(d.message),d.accept()))
 page.route('**/api/status',lambda r:r.fulfill(json={'configured':True,'model':'SIMULADO','transcribeModel':'SIMULADO','token':'test-only'}))
 page.route('**/api/generate',generate)
 page.goto(f'http://127.0.0.1:{server.server_port}/')
 page.locator('#source-url').fill('https://youtu.be/dQw4w9WgXcQ');page.locator('#youtube-source').click()
 assert 'No puedo descargar' in page.locator('#ai-status').inner_text()
 page.locator('#ai-consent').check();page.locator('#generate').click()
 assert 'transcripción' in page.locator('#ai-status').inner_text() and not requests
 page.locator('#transcript').fill(source);page.locator('#question-count').fill('2');page.locator('#difficulty').select_option('intermedia')
 page.reload();assert page.locator('#transcript').input_value()==source
 page.locator('#ai-consent').check();page.locator('#question-count').fill('2');page.locator('#difficulty').select_option('intermedia')
 page.locator('#generate').click();page.locator('#accept-draft').wait_for()
 assert requests[-1]['count']==2 and requests[-1]['difficulty']=='intermedia' and requests[-1]['types']=='mixed'
 assert source[:57] in page.locator('#ai-draft').inner_text()
 page.locator('[data-objective="O1"]').fill('Identificar el paso del agua líquida a vapor')
 page.locator('#accept-draft').click()
 assert page.locator('.select-item').count()==2
 assert 'paso del agua' in page.locator('#objectives').input_value()
 page.locator('#gift').click();assert 'revisa' in alerts[-1]
 page.locator('[data-field="title"]').fill('¿Qué cambio produce el calor en el agua líquida?')
 page.locator('[data-field="reviewed"]').check()
 page.locator('[data-field="feedbackIncorrect"]').fill('El agua pasa a vapor; no se transforma en metal o piedra ni desaparece.')
 assert not page.locator('[data-field="reviewed"]').is_checked()
 page.locator('[data-field="reviewed"]').check()
 page.locator('.select-item').nth(1).click();page.locator('[data-field="reviewed"]').check()
 with page.expect_download() as info:page.locator('#gift').click()
 target=BASE/'work/ia-preguntas.gift';info.value.save_as(target)
 gift=target.read_text();assert 'El agua pasa a vapor' in gift and '{TRUE#' in gift
 with page.expect_download() as info:page.locator('#save').click()
 target=BASE/'work/ia-editable.json';info.value.save_as(target)
 data=json.loads(target.read_text());assert data['sources'][0]['transcript']==source and data['items'][0]['reviewed']
 page.locator('#preview').click();page.locator('#start').click();page.locator('[data-answer="1"]').click()
 assert page.locator('[data-answer="0"]').is_disabled() and 'no se transforma' in page.locator('#feedback').inner_text()
 page.locator('#close').click();page.locator('#preview').click();assert page.locator('[data-answer="0"]').is_disabled()
 page.locator('#next').click();page.locator('[data-answer="0"]').click();page.locator('#next').click()
 assert page.locator('#restart').count()==0 and 'No se permite volver' in page.locator('#student-body').inner_text()
 page.locator('#close').click()
 page.locator('#transcript').fill('SIN CONTENIDO '*20);page.locator('#generate').click()
 page.wait_for_function("document.getElementById('ai-status').textContent.includes('insuficiente')")
 assert page.locator('.select-item').count()==2 and page.locator('#accept-draft').count()==0
 page.route('**/api/transcribe',lambda r:r.fulfill(status=400,json={'error':'Audio no disponible.'}))
 page.locator('#source-file').set_input_files({'name':'video.mp4','mimeType':'video/mp4','buffer':b'not-real-video'})
 page.locator('#transcribe').click();page.wait_for_function("document.getElementById('ai-status').textContent.includes('Audio no disponible')")
 assert 'manualmente' in page.locator('#ai-status').inner_text()
 page.route('**/api/transcribe',lambda r:r.fulfill(json={'transcript':source}))
 page.locator('#transcribe').click();page.wait_for_function("document.getElementById('ai-status').textContent.includes('Audio transcrito')")
 assert page.locator('#transcript').input_value()==source
 page.locator('#file').set_input_files(str(target));assert page.locator('.select-item').count()==2
 page.screenshot(path=str(BASE/'work/interfaz-ia.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 assert not errors,errors
 browser.close()
server.shutdown()
print('OK: IA simulada, YouTube sin transcripción, fuente persistente, cantidad/dificultad, objetivos editables, aprobación, exportación, JSON, único intento, error de IA y transcripción con recuperación manual.')
