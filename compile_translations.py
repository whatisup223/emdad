#!/usr/bin/env python3
"""
Compile translation files manually
"""

import os
import struct

def compile_po_to_mo(po_file, mo_file):
    """Compile .po file to .mo file using msgfmt-like approach"""

    print(f"Compiling {po_file} to {mo_file}")

    # Use pybabel if available, otherwise manual compilation
    try:
        import subprocess
        result = subprocess.run(['msgfmt', po_file, '-o', mo_file],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Compiled using msgfmt: {mo_file}")
            return
    except:
        pass

    # Manual compilation
    # Read .po file
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse translations using simple regex
    import re

    # Find all msgid/msgstr pairs
    pattern = r'msgid\s+"([^"]*(?:"[^"]*"[^"]*)*)"\s*msgstr\s+"([^"]*(?:"[^"]*"[^"]*)*)"'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

    translations = {}
    for msgid, msgstr in matches:
        # Clean up the strings
        msgid = msgid.replace('\\"', '"').replace('\\n', '\n')
        msgstr = msgstr.replace('\\"', '"').replace('\\n', '\n')

        if msgid and msgstr:  # Only add non-empty translations
            translations[msgid] = msgstr

    print(f"Found {len(translations)} translations")

    # Print some key translations for verification
    key_translations = ['Admin Login', 'Email Address', 'Password', 'Remember me', 'Sign In']
    for key in key_translations:
        if key in translations:
            print(f"  ✅ {key} → {translations[key]}")
        else:
            print(f"  ❌ Missing: {key}")
    
    # Create .mo file
    os.makedirs(os.path.dirname(mo_file), exist_ok=True)
    
    # Simple .mo file format
    with open(mo_file, 'wb') as f:
        # Magic number
        f.write(struct.pack('<I', 0x950412de))
        # Version
        f.write(struct.pack('<I', 0))
        # Number of strings
        f.write(struct.pack('<I', len(translations)))
        # Offset of table with original strings
        f.write(struct.pack('<I', 28))
        # Offset of table with translation strings  
        f.write(struct.pack('<I', 28 + len(translations) * 8))
        # Hash table size
        f.write(struct.pack('<I', 0))
        # Offset of hash table
        f.write(struct.pack('<I', 0))
        
        # Calculate string offsets
        offset = 28 + len(translations) * 16
        
        # Write original string table
        for msgid in translations.keys():
            msgid_bytes = msgid.encode('utf-8')
            f.write(struct.pack('<I', len(msgid_bytes)))
            f.write(struct.pack('<I', offset))
            offset += len(msgid_bytes)
        
        # Write translation string table
        for msgstr in translations.values():
            msgstr_bytes = msgstr.encode('utf-8')
            f.write(struct.pack('<I', len(msgstr_bytes)))
            f.write(struct.pack('<I', offset))
            offset += len(msgstr_bytes)
        
        # Write original strings
        for msgid in translations.keys():
            f.write(msgid.encode('utf-8'))
        
        # Write translation strings
        for msgstr in translations.values():
            f.write(msgstr.encode('utf-8'))
    
    print(f"✅ Compiled {mo_file}")

def main():
    """Compile all translation files"""
    
    print("🔄 Compiling translation files...")
    
    # Arabic
    ar_po = 'translations/ar/LC_MESSAGES/messages.po'
    ar_mo = 'translations/ar/LC_MESSAGES/messages.mo'
    
    if os.path.exists(ar_po):
        compile_po_to_mo(ar_po, ar_mo)
    else:
        print(f"❌ {ar_po} not found")
    
    # English
    en_po = 'translations/en/LC_MESSAGES/messages.po'
    en_mo = 'translations/en/LC_MESSAGES/messages.mo'
    
    if os.path.exists(en_po):
        compile_po_to_mo(en_po, en_mo)
    else:
        print(f"❌ {en_po} not found")
    
    print("✅ Translation compilation complete!")

if __name__ == "__main__":
    main()
