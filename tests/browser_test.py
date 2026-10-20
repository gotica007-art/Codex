from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import http.server, threading, functools
server=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parents[1])))
threading.Thread(target=server.serve_forever,daemon=True).start()
BASE=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1280,'height':1000},accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('dialog',lambda d:d.accept())
    page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
    page.locator('#title').fill('El ciclo del agua')
    page.locator('#description').fill('Aprendemos con ejemplos')
    page.locator('#objectives').fill('Identificar la evaporación')
    page.locator('[data-add="content"]').click()
    page.locator('[data-field="title"]').fill('Evaporación')
    page.locator('[data-field="text"]').fill('El agua pasa a vapor.')
    page.locator('[data-field="example"]').fill('Un charco al sol.')
    page.locator('[data-add="multiple"]').click()
    page.locator('[data-field="title"]').fill('¿Qué produce el calor?')
    for k,a in enumerate(['Evaporación','Congelación','Nada','Nieve']):page.locator(f'[data-field="option{k}"]').fill(a)
    page.locator('[data-add="boolean"]').click()
    page.locator('[data-field="title"]').fill('El agua puede evaporarse')
    page.locator('[data-field="feedbackCorrect"]').fill('¡Exactamente!')
    page.locator('[data-up]').last.click()
    assert 'El agua puede evaporarse' in page.locator('.select-item').nth(1).inner_text()
    page.locator('[data-down]').nth(1).click()
    page.reload()
    assert page.locator('#title').input_value()=='El ciclo del agua'
    assert page.locator('.select-item').count()==3
    page.locator('#preview').click();page.locator('#start').click();page.locator('#next').click()
    page.locator('[data-answer="1"]').click()
    assert 'incorrecta' in page.locator('#feedback').inner_text()
    assert page.locator('#next').is_enabled()
    assert page.locator('[data-answer="0"]').is_disabled()
    page.locator('#next').click()
    page.locator('[data-answer="0"]').click()
    assert '¡Exactamente!' in page.locator('#feedback').inner_text()
    page.locator('#next').click()
    assert 'completada' in page.locator('#student-body').inner_text()
    assert page.locator('#restart').count()==0
    page.locator('#close').click();page.locator('#preview').click()
    assert 'completada' in page.locator('#student-body').inner_text()
    page.locator('#close').click()
    for id,name in [('gift','preguntas.gift'),('guide','guia-de-contenido.html'),('save','leccion-editable.json')]:
        with page.expect_download() as info:page.locator('#'+id).click()
        dest=BASE/'work'/name;info.value.save_as(dest)
        assert dest.stat().st_size>0
    gift=(BASE/'work/preguntas.gift').read_text()
    assert 'Evaporación::' not in gift and '{TRUE#' in gift and '=Evaporación#' in gift
    guide=(BASE/'work/guia-de-contenido.html').read_text()
    assert 'Un charco al sol.' in guide and 'El agua puede evaporarse' in guide
    page.locator('#new').click()
    page.locator('#file').set_input_files(str(BASE/'work/leccion-editable.json'))
    assert page.locator('#title').input_value()=='El ciclo del agua'
    assert page.locator('.select-item').count()==3
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not errors,errors
    browser.close()
print('OK: edición, tres tipos, orden, persistencia, vista previa, feedback, tres descargas, reapertura y diseño móvil. Sin errores JavaScript.')
