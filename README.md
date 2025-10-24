# pydefold
defold proto compiled to python (check branches of this repo for already build protofiles , is under folder "defoldsdk")



## How  : 
to build defold desired version protofile into python modules "defoldsdk"  : 
1-  select version in $version=1.11.1 in line 4 in [scripts/build.sh](scripts/build.sh) : 
```bash
#!/bin/bash
set -euo pipefail
file_path=
version=1.11.1 # <-- this line , see scripts/build.sh
git_root=$(git rev-parse --show-toplevel)
```
2 - then run make 
```bash
make
```
you will have folder called *defoldsdk*  !!

## Usage 
all proto objects are under the namespace sdk 
```python
from  defoldsdk import sdk 

for i in sdk : 
    print(i)

x = sdk.Texture()
```
example load collection from string 
```python
from  defoldsdk import sdk 
from google.protobuf.json_format import MessageToJson
from google.protobuf.text_format import MessageToString, Parse

content = '''
name: "menu"
scale_along_z: 0
embedded_instances {
  id: "go"
  data: "components {\\n"
  "  id: \\"menu\\"\\n"
  "  component: \\"/examples/collection/proxy/menu.gui\\"\\n"
  "  position {\\n"
  "    x: 0.0\\n"
  "    y: 0.0\\n"
  "    z: 0.0\\n"
  "  }\\n"
  "  rotation {\\n"
  "    x: 0.0\\n"
  "    y: 0.0\\n"
  "    z: 0.0\\n"
  "    w: 1.0\\n"
  "  }\\n"
  "}\\n"
  ""
  position {
    x: 0.0
    y: 0.0
    z: 0.0
  }
  rotation {
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
  }
  scale3 {
    x: 1.0
    y: 1.0
    z: 1.0
  }
}
'''


collection = sdk.CollectionDesc()
Parse(content.encode('utf-8'), collection)
print(MessageToString(collection))
print(MessageToJson(collection,preserving_proto_field_name=True))
```

```log
name: "menu"
scale_along_z: 0
embedded_instances {
  id: "go"
  data: "components {\n  id: \"menu\"\n  component: \"/examples/collection/proxy/menu.gui\"\n  position {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n  }\n  rotation {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n    w: 1.0\n  }\n}\n"
  position {
    x: 0.0
    y: 0.0
    z: 0.0
  }
  rotation {
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
  }
  scale3 {
    x: 1.0
    y: 1.0
    z: 1.0
  }
}

{
  "name": "menu",
  "scale_along_z": 0,
  "embedded_instances": [
    {
      "id": "go",
      "data": "components {\n  id: \"menu\"\n  component: \"/examples/collection/proxy/menu.gui\"\n  position {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n  }\n  rotation {\n    x: 0.0\n    y: 0.0\n    z: 0.0\n    w: 1.0\n  }\n}\n",
      "position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
        "w": 1.0
      },
      "scale3": {
        "x": 1.0,
        "y": 1.0,
        "z": 1.0
      }
    }
  ]
}```
