Reference [here](https://github.com/gSchool/dsi-high-performance-python/blob/master/individual.md) on Part 2

## EC2 on AWS

EC2 is a remote virtual machine that runs programs much like your local machine. Here you will learn how to
run tasks on an EC2 machine. Most EC2 instances come without a lot of the packages you need. Here, we will use
an instance that has most of the data science packages installed.

<br>

1. Create an EC2 instance. Choose `t2.micro` for the instance type and Ubuntu 16.04 as the operating system. Give the instance an IAM role that allows it full access to S3. Choose an *all-lowercase* name for the instance and add a `Name` tag (Key=`Name`, Value=`examplename`). Careful: Do not replace `Name` in the key field. Set the value instead by replacing `examplename`.
  
2. Add the instance to your `~/.ssh/config` file, but replace `examplename` with the actual name, replace the HostName with the actual public DNS, and replace `example.pem` with your real `.pem` file.
.

```
Host examplename
 HostName 52.27.155.84
 User ubuntu
 IdentityFile ~/.ssh/example.pem
```
3. Log into the instance you have launched using `ssh`. 

```
ssh examplename
```

4. Update `apt` sources and perform routine updates:

```
sudo apt update
sudo apt upgrade
```

5. Install Anaconda & MongoDB

```
# create anacoda folder
mkdir anacoda

# Download Anaconda3
wget -S -T 10 -t 5 https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh -O $HOME/anaconda/anaconda.sh

# Install Anaconda
bash $HOME/anaconda/anaconda.sh -u -b -p $HOME/anaconda

# Add Anaconda to current session's PATH
export PATH=$HOME/anaconda/bin:$PATH

# Add Anaconda to PATH for future sessions via .bashrc
echo -e "\n\n# Anaconda" >> $HOME/.bashrc
echo "export PATH=$HOME/anaconda/bin:$PATH" >> $HOME/.bashrc

# install MongoDB
conda install -c anaconda mongodb 

# install pymongo
conda install -c anaconda pymongo
```

6. Install required AWS libraries

```
pip install awscli boto3
```

7. Start MongoDB

```
sudo service mongod start
```
If there is error, try to follow [this link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition) to solve it.

8. Create MongoDB

```
# navigate to aws_app/src directory and execute
python mongo_subset.py
```

9. Start Web page

```
# navigate to aws_app directory and excute
python yelp_app.py
```
Now in your preferred browser, type `52.27.155.84:5000`, replace `52.27.155.84` with your acural value from `step 2` above. Some user id to try with: `--Nnm_506G_p8MxAOQna5w`, `--2HUmLkcNHZp0xw6AMBPg`, `-0IiMAZI2SsQ7VmyzJjokQ`

