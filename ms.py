# OCR - Project Oxford by MS
from PIL import Image
import httplib, urllib, base64, json
import cv2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def print_text(json_data):
    g = open('word.txt', 'w')
    result = json.loads(json_data)
    for l in result['regions']:
        for w in l['lines']:
            line = []
            for r in w['words']:
                line.append(r['text'])
            # print ' '.join(line) ###########detected korean
            g.write(' '.join(line))
            g.write('\n')
    g.close()
    return

def print_box(json_data):
    f = open('box.txt', 'w')
    result = json.loads(json_data)
    line = []
    for l in result['regions']:
        for w in l['lines']:
            line.append(w['boundingBox'])

    # print '\n'.join(line) ###########detected text box position
    f.write(str('\n'.join(line)))

    f.close()
    return


def ocr_project_oxford(headers, params, data):
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, data, headers=headers)
    response = conn.getresponse()
    data = response.read()
    # print data + "\n"
    #
    # parsed = json.loads(data)
    # print (json.dumps(parsed, sort_keys=True, indent=2))

    print_text(data) # print recognized words
    print_box(data) # print text box
    conn.close()
    return

if __name__ == '__main__':
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '84cc2c01bd414f25ac6f7735eeb05afb',
    }
    params = urllib.urlencode({
        # Request parameters
        'language': 'ko',   #korean
        'detectOrientation ': 'ture',
    })
    name = str(sys.argv[1])

    data = open('images/'+name, 'rb').read()


    try:
        image_file ='images/'+name
        # im = Image.open(image_file)
        #im.show()
        ocr_project_oxford(headers, params, data)

        original = cv2.imread(image_file,cv2.IMREAD_COLOR)
        original2=cv2.imread(image_file,cv2.IMREAD_COLOR)
        # cv2.imshow('original ', original)

        f = open('box.txt')
        txt = f.read()
        t = re.split(",|\n", txt)
        #print t

        for i in range(0, len(t), 4):
            # print t[i], t[i + 1], t[i + 2], t[i + 3]
            cv2.rectangle(original, (int(t[i]),int(t[i + 1])), (int(t[i])+int(t[i + 2]),int(t[i + 1])+int(t[i + 3])), (255,255,255),-1,1,0)
            cv2.rectangle(original2, (int(t[i]),int(t[i + 1])), (int(t[i])+int(t[i + 2]),int(t[i + 1])+int(t[i + 3])), (255,0,255),1,1,0)

        cv2.imshow('detect',original2)
        cv2.imshow('remove', original)
        cv2.imwrite('result_'+name,original)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(1)


    except Exception as e:
        print(e)