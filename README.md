# A-Fat-Tree-Topology-of-Scalable-Data-Center-Network-using-SDN
My first repository
---------------------------
Instruction:
The running process is tricky and trivial, and there is a lot of things to configure.
Here is a brief instruction how to do it. 

1. Git clone Mininet on the Ubuntu(Strongly recommend VirtualBox, rather 
than Paralles, otherwise there are little problem about etho connection when you running)

2. We have replace the file floodlight/src/main/java/net/
floodlightcontroller/learningswitch with our own file. In Mac 
Terminal(Not virtual machine running Miniet), just run:

   cd ~/floodlight-0.91
   ant
   java -jar target/floodlight.jar

   Before this, you may need to use Eclipse to load the module. After running the 
above code, the floodlight can work, and listen on default port:6633

3. In the Mac Terminal, use ifconfig to find your IP address. And change 
the controller IP in fattree.py with what you find(Maybe not etho0 as default). 

In Mininet, run:
   sudo python fattree.py
  
Then it will work. 

Enjoy.
