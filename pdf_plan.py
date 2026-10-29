import sys, json, base64, io

try:
    import pypdfium2 as pdfium
    body = json.load(sys.stdin)
    raw = base64.b64decode(body['pdf'].split(',', 1)[1], validate=True)
    if len(raw) > 20 * 1024 * 1024 or not raw.startswith(b'%PDF-'):
        raise ValueError('Use a valid PDF under 20 MB.')
    doc = pdfium.PdfDocument(raw)
    count = len(doc)
    page_number = body['page']
    if not 1 <= page_number <= count:
        raise ValueError(f'Choose a page from 1 to {count}.')
    page = doc[page_number - 1]
    scale = min(2.5, 2200 / max(page.get_size()))
    bitmap = page.render(scale=scale)
    image = bitmap.to_pil()
    output = io.BytesIO()
    image.save(output, format='PNG')
    print(json.dumps({'image': 'data:image/png;base64,' + base64.b64encode(output.getvalue()).decode(), 'pages': count, 'page': page_number}))
    bitmap.close()
    page.close()
    doc.close()
except Exception as exc:
    message = str(exc) if isinstance(exc, ValueError) else 'Could not read this PDF. Use an unencrypted PDF or upload a PNG/JPG plan.'
    print(json.dumps({'error': message}))
    sys.exit(1)
