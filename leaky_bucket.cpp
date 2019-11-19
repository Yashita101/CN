#include<iostream>
#include<unistd.h>
#include<stdlib.h>
#define bs 512
using namespace std;
void bktInput(int a, int b);
int main()
{
int op,pktsize;
cout<<"Enter op rate";
cin>>op;
for(int i=1;i<=5;i++)
{
usleep(rand()%1000);
pktsize=rand()%1000;
cout<<"\n Packet no."<<i<<"\t Packet size="<<pktsize;
bktInput(pktsize,op);
}
return 0;
}
void bktInput(int a, int b)
{
if(a>bs)
	cout<<"\n\t\t Bucket Overflow";
else
{
usleep(500);
while(a>b)
{
	cout<<"\n\t\tLast"<<a<<"bytes outputted";
	a-=b;
	usleep(500);
}
if(a>0)
cout<<"\n\t\tLast"<<a<<"bytes sent \t";
cout<<"\n\t\t Bucket op successful";
}}
