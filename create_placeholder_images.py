import base64

blank_png = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAC1+jfqAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAH1JREFUeNrs0TEBAAAIwqD1T20ND6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB4GgAAAZH7BtwAAAAASUVORK5CYII='
)

for filename in ['6b_deployment_test.png', '7c_error_handling_interface.png']:
    with open(filename, 'wb') as image_file:
        image_file.write(blank_png)

print('created placeholder images')
