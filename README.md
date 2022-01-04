# Python sample API scripts
A set of sample calls to the Meterian API in Python: use simple python scripts to leverage the power of the [Meterian API](http://api.meterian.io). You will need to install the 'requests' python library, or you can just use the provided 'requirements.txt' file. This version uses Python 2.

## You will need a token to use these tools!

All these tools will require an API token from Meterian. This is available for any paid plan, and it can be generated at  https://meterian.com/account/#tokens

Once you have the token, the best and secure way to use it is to put it into an environment variable, called METERIAN_API_TOKEN. In linux, for example, you can simply do something like this:

    export METERIAN_API_TOKEN=a902874d-50f2-464f-8707-780cd5f669a3
(no, this is not a real token eheh!)

In most of the commands however you can simply specify the token on the command line using something like this:

    ./yadda.py --token=a902874d-50f2-464f-8707-780cd5f669a3

# Tools

## license&#46;py
This script allows you to list the licenses of a component across [the platforms managed by Meterian](https://www.meterian.com/integrations.html#languages) . Simply specify the language, the full name of the library and the version: the tool will let you know the licenses found. Sometime it's instant, sometimes it may take a couple of seconds: do not worry, a result will eventually come :)

Asking for **java** library, **io.vertx:vertx-core**, version **3.9.1**

    $ ./license.py java io.vertx:vertx-core 3.9.1
        Looking for license information about "io.vertx:vertx-core" version "3.9.1" in the "java" space...
        Found 2 license(s):
        - id:   Apache-2.0
          name: Apache License 2.0
          uri:  https://spdx.org/licenses/Apache-2.0.html
        - id:   EPL-2.0
          name: Eclipse Public License 2.0
          uri:  https://spdx.org/licenses/EPL-2.0.html

Asking for **nodejs** library, **less**, version **3.11.3**

    $ ./license.py nodejs less 3.11.3
    Looking for license information about "less" version "3.11.3" in the "nodejs" space...
    Found 1 license(s):
    - id:   Apache-2.0
      name: Apache License 2.0
      uri:  https://spdx.org/licenses/Apache-2.0.html

## vulninfo&#46;py
This script allows you to list information regarding a specific vulnerability across Meterian curated advisories databases (php, nvd, gha). Simply specify the latter database and the unique identifer for a given vulnerability and the tool will fetch relevant information about it.

Asking for vulnerability **CVE-2020-9483** from the **nvd** database

```bash
$ ./vulninfo.py nvd CVE-2020-9483
Fetching information for vulnerability "CVE-2020-9483" from the "java" database...
- id:               d192e5ad-5948-4bd8-8d00-3c05e83abd17
  library:          org.apache.skywalking:server-storage-plugin
  language:         java
  version range:    [6.0.0,8.0.0)
  severity:         MEDIUM
  links:            https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-9483
                    https://nvd.nist.gov/vuln/detail/CVE-2020-9483
                    https://github.com/apache/skywalking/pull/4639

  source:           METERIAN
  type:             SECURITY
  cvss:             5
  active:           False
  fixed version(s): [8.0.0]
  description:      **Resolved** When use H2/MySQL/TiDB as Apache SkyWalking storage, the metadata query through GraphQL protocol, there is a SQL injection vulnerability, which allows to access unpexcted data. Apache SkyWalking 6.0.0 to 6.6.0, 7.0.0 H2/MySQL/TiDB storage implementations don't use the appropriate way to set SQL parameters.
```

## advisories&#46;py
This script allows to list the advisories of associated to a given library. After specifying the language, the full name fo the library and its version, the tool will fetch all the related advisories it can find.

Asking for **dotnet** library, **System.Text.RegularExpressions**, version **4.3.0**

```bash
$ ./advisories.py dotnet System.Text.RegularExpressions 4.3.0
Looking for advisories for "System.Text.RegularExpressions" version "4.3.0" in the "dotnet" space...
Found 1 advisory:
- id:                  3fbb34a8-ee91-4774-a059-d5452b79d159
  library:             system.text.regularexpressions
  language:            dotnet
  version range:       [4.3.0,4.3.1)
  severity:            HIGH
  links:               https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-0820
                      https://nvd.nist.gov/vuln/detail/CVE-2019-0820
                      https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-0820
                      https://github.com/dotnet/core/blob/master/release-notes/2.2/2.2.5/2.2.5.md

  source:              METERIAN
  type:                SECURITY
  cwe:                 CWE-400
  cvss:                7.5
  active:              False
  fixed in version(s): [4.3.1]
  description:         A denial of service vulnerability exists when .NET Core improperly process RegEx strings. An attacker who successfully exploited this vulnerability could cause a denial of service against a .NET application. A remote unauthenticated attacker could exploit this vulnerability by issuing specially crafted requests to a .NET Core application.
```

## Help
If in need of help issue the `--help` flag (all the listed tools support it).

    $ ./license.py --help
    usage: license.py [-h] [-t API-TOKEN] [-l LOGLEVEL] language name version

    positional arguments:
      language              The language of the library (i.e. java) ['java',
                            'javascript', 'nodejs', 'python', 'dotnet', 'ruby',
                            'scala', 'php', 'swift', 'golang']
      name                  The full name of the library (i.e.
                            com.fasterxml.jackson.core:jackson-databind)
      version               The version of the library (i.e. 2.8.8)

    optional arguments:
      -h, --help            show this help message and exit
      -t API-TOKEN, --token API-TOKEN
                            Allows you to specify the API token to use directly on
                            the command line. You can create your token with a
                            bootstrap+ plan at
                            https://meterian.com/account/#tokens
      -l LOGLEVEL, --log LOGLEVEL
                            Sets the logging level (default is warning)


# Other general information
## Common parameters
As a common beheaviour across all the tools, it's also possible to specify the log level with any tool using  soething like this:

    ./yadda.py --log=DEBUG
Beware: the DEBUG level can be very verbose!


## What's more?
Well. you can build your onw tool using the Meterian API at https://api.meterian.io and you can also contribute to this repository!
