import sys
import base64

def convert_from_base64(encoded_data):
    return base64.b64decode(encoded_data).decode('utf-8')

def convert_from_hex(encoded_data):
    return bytes.fromhex(encoded_data).decode('utf-8')

def convert_from_byte(encoded_data):
    # Sử dụng 'unicode_escape' để giải mã chuỗi byte escape
    return encoded_data.encode('utf-8').decode('unicode_escape')

def convert_from_binary(encoded_data):
    binary_values = [encoded_data[i:i+8] for i in range(0, len(encoded_data), 8)]
    byte_data = bytes([int(b, 2) for b in binary_values])
    return byte_data.decode('utf-8')

def main():
    if len(sys.argv) != 3:
        print("Usage: python task_2.py <format> <input>")
        print("<format> should be one of: base64, hex, byte, binary")
        sys.exit(1)
    
    format_type = sys.argv[1].lower()
    input_data = sys.argv[2]
    
    try:
        if format_type == 'base64':
            result = convert_from_base64(input_data)
        elif format_type == 'hex':
            result = convert_from_hex(input_data)
        elif format_type == 'byte':
            result = convert_from_byte(input_data)
        elif format_type == 'binary':
            result = convert_from_binary(input_data)
        else:
            print("Error: Unsupported format. Choose from base64, hex, byte, binary.")
            sys.exit(1)
        
        print("Result:", result)
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

if __name__ == "__main__":
    main()
