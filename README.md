
### COSC 465 Final Project            
### Tori Gobo, Sara Alan, Jin Sohn, Kate Valente 

# Analyzing Colgate's Network Traffic
## DESCRIPTION
The main goal of this project is to analyze Colgate’s internet traffic patterns in a way that aids in the 
maintenance and betterment of the campus’ network. To do this, Colgate’s Information and Technological Services Department 
(ITS) provided our group with SFlow data from the virtual local area network (VLANs) of several institutions on campus 
(i.e. guest, student, faculty, and staff wireless). From these packets, we can determine which institutions use Colgate’s network 
the most, and we can use the destination IPs embedded in the SFlow data to learn more about what addresses were contacted 
outside the network. Understanding these qualities can provide insights into who exactly is using the majority of the network, 
and what websites they are looking for, which can be applied to Colgate's Network to better network efficiency and functionality. 

## INSTRUCTIONS
For this project, there are three .py files that need to be run: readnfcap.py, getDN.py and
getCat.py. In addition, a separate repository must be used first in order to transform the SFlow data into a 
format that can be easily read (.txt). This repository is linked here: https://github.com/phaag/nfdump


Once the SFlow data is transformed into a .txt file, the following sequence of python files can be run.


### 1.) readnfcap.py
        Input: <br>
            SFlow data in the .txt format <br>
        Output: <br>
            .txt files of tuples containing the source ips, the destination ips and the sum of bytes for each packet <br>
        Description: <br>
            The purpose of this file is to retrieve what is needed from the sflow data. The SFlow data is separated
            into folders corresponding to the dates in which the data was captured. These folders were read in 
            line 17, and for each file in the folder we ran the function getIP. getIP takes the filename, directory and output file, and writes in all
            the tuples containing the source ips, the destination ips and the sum of bytes for each packet in the outfile. Since we only want the 
            source/destination IP, and bytes exchanged, we use the headers in the SFlow data to find the corresponding column numbers. In our case, 
            it is 3,4, 12, and 14. The output returns .txt files containing these tuples. <br>

### 2.) getDN.py
Method: main(): <br>
    Description: <br>
        The main method first reads in the .txt files containing tuples obtained in readnfcap.py and uses reverse DNS on the 
            source and destination IPs to obtain the domain names. While the domain names are gathered, it checks if the domain name
            has already been added to a file of unique domain names. If not, it is added. If the reverse DNS lookup did not work
            it is added to a list of failed DNS lookups. The result should be a unique list of domain names that can be analyzed.
            Different functions highlighted below conduct this analysis.  <br>
Method: getAllDNs(): <br>
    Output:  <br>
        a text file containing all the Domain names in one list <br>
Method: getIP(): <br>
    Input:  <br>
        source and destination IP addresses from tuple, bytes exchanged <br>
    Output: <br>
        returns which IP (source or destination) to check the Domain Name of, for a single sflow record <br>
    Description: <br>
        picks IPs external to Colgate when possible. if both source and destination are Colgate IPs, picks the source. 
            Updates frequency of flow for each colgate subnet. <br>
Method: IsColgate(): <br>
    Input: <br>
        is a list of numbers corresponding to a single IPv4 address where each element is one of the 8-bit sets from the 
        IPv4 address(from left to right) <br>
    Output: <br>
        returns true if the address is part of the IPv4 address range owned by Colgate <br>
Method: findSubnet(): <br>
    Input: <br>
        is the number in the 3rd 8 bits of an IPv4 address <br>
    Output: <br>
        returns an index corresponding to the Colgate subnet the address belongs to
        the index is relative to the list of subnets on line 95 in the main function <br>
    Description: <br>
        Finds the corresponding subnet from the colgate IP address. Subnets were provided by Colgate's ITS. <br>

### 3.) getCat.py
#### IN ORDER TO RUN THIS METHOD YOU MUCT CREATE A KLAZIFY ACCOUNT FROM THE WEBSITE HERE: "https://www.klazify.com/register" AND GET AN API KEY <br>
    Input: <br>
        Domain Names from .txt files
        Output: 
            .txt files of the domain names and what categories they were classified as
        Description: 
            First run the divide100DNs() method in order to get the data into an amount that can be run with the website. 
            Next run getCat() in order to get the categorization of each of these domains. 
            This method posts the domain name for a specific query onto a website called 'Klazify' 
            which categorizes the domain name into one of over 385 distinct categories. 'Klazify' can only run 100
            domain names for free on their website, and that is why the domain names need to be separated. 
            Also, two lines need to be changed in this code to run. The first is line 44, in which the text
            after the word 'Bearer' needs to be changed to be the API key given after making a membership with Klazify. 
            The second line, line 71, need to have its file name changed to the corresponding text file that has the domain names
            that you want to categorize from. The output of this method is the domain names and categories written into a .txt 

            


