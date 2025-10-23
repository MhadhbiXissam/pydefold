# pydefold
defold proto compiled to python



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