### Simple POS
Simple POS provides a streamlined and clean registry interface for small business. 

### Installation
<b>Windows</b>

In order to run OnkoDICOM on Windows, you will need to have installed:

64-bit Python 3.7 or later. SimplePOS will not run on 64-bit computers that have a 32-bit version of Python installed. Additionally, OnkoDICOM has not been tested on 32-bit machines.
Visual Studio Build Tools
If you do not already have virtualenv installed into your global packages, execute the command:

<pre><code>pip install virtualenv</pre></code>

First, clone the OnkoDICOM repository and switch to it:
<pre><code>git clone https://github.com/didymo/OnkoDICOM.git
cd OnkoDICOM</code></pre>
Then, create and activate the virtual environment:

<pre><code>python -m virtualenv venv
venv\Scripts\activate</pre></code>


Once you are within the virtual environment, install the requirements:

<pre><code>pip install -r pre-requirements.txt
pip install -r requirements.txt</pre></code>

After the requirements are installed, you can run Sime POS with the command:

<pre><code>python main.py</pre></code>

