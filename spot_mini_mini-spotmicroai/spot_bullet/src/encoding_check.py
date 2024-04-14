import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    return chardet.detect(rawdata)

file_path = '/home/kom018/spot_mini_mini-spotmicroai/spot_bullet/models/spot_ars_19_policy'
result = detect_encoding(file_path)
print("Detected encoding:", result['encoding'])



def detect_encoding_with_bom(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        if rawdata.startswith(b'\xef\xbb\xbf'):
            return 'UTF-8 with BOM'
        elif rawdata.startswith(b'\xff\xfe'):
            return 'UTF-16 LE'
        elif rawdata.startswith(b'\xfe\xff'):
            return 'UTF-16 BE'
        elif rawdata.startswith(b'\x00\x00\xfe\xff'):
            return 'UTF-32 BE'
        elif rawdata.startswith(b'\xff\xfe\x00\x00'):
            return 'UTF-32 LE'
        else:
            return 'Unknown or no BOM detected'

# file_path = 'path_to_your_file'
result = detect_encoding_with_bom(file_path)
print("Detected encoding:", result)
