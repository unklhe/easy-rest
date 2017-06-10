# Easy Rest
This is a wraping of python urllib2 to quickly access Rest API.
SSL is supported by disabling the certificate verifcation.

# Requirements
* Python 2.7.6+ or Python 3.0 +

# Installation
Install stable version
```bash
pip install easyrest
```

or install develop version
```bash
python setup.py install
```


# Usage
Try CRUD directely
```python
from easy_rest import *

resp = get("http://yourserver/url")
print resp.read()

get("http://yourserver/url", Authorization="dGVzdDp0ZXN0")

post("http://yourserver/url", {"key": "value"})

```

Use a connection object
```python
client = Connection("yourserver", "/",
                auth_type="basic",
                auth_user="test",
                auth_password="test")
resp = client.get("/url")
print resp.body

client.post("/url/id", "a=b&c=d")

client.delete("/url/id")
```


# License
Copyright 2017 Eric.He

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
