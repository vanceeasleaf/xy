#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
using namespace std;
void xymodel(int l,int q);
double *e1;
void calculate(int l,int q,double t,double *sumh,double *sumh2,double *summ,double *summ2);
int main()
{
    xymodel(32,4);
    return 0;
}

void xymodel(int l,int q)
{
    FILE *fp;
    double t=.01,tstart=.1,tend=1.50,deltat=.01,sumh=0,sumh2=0,c=0,summ=0,summ2=0,x=0;
    printf("#condition:(l=%d,q=%d),start simulating,please wait.\n",l,q);
    printf("temperature\tenergy\theat_capacity\tmagnetization\tsusceptibility\n");
    fp=fopen("result_xymodel.txt","w");
    fprintf(fp,"#resultof(L=%d,Q=%d):\n",l,q);
    fprintf(fp,"temperature\tenergy\theat_capacity\tmagnetization\tsusceptibility\n");
    e1=new double[100000];
    for(t=tstart; t<=tend; t+=deltat)
        {
            deltat=(t<.6)?.05:((t<1.0)?0.005:0.05);
            calculate(l,q,t,&sumh,&sumh2,&summ,&summ2);
            c=(sumh2-sumh*sumh)/(4*t*t);
            double s=0;
            double s2=0;
            for(int i=50000;i<=100000;i++){
            s+=e1[i];

            }
            s/=50000;
            for(int i=50000;i<=100000;i++){
            s2+=(e1[i]-s)*(e1[i]-s);
            }
            s2/=50000*(4*t*t);
            x=(summ2-summ*summ)/t;
            fprintf(fp,"%f\t%f\t%f\t%f\t%f\t%f\t%f\n",t,sumh/2,s/2,c,s2/2,summ,x);
            printf("%f\t%f\t%f\t%f\t%f\t%f\t%f\n",t,sumh/2,s/2,c,s2/2,summ,x);
        }
    fclose(fp);
}
int isMK(int x,int y)
{
    return(x==0&&y==0)?1:0;
}
double delta(int x,int y)
{
    return (x==y)?1:0;
}
double random1()
{
    int i;
    double x=0;
    for(i=1; i<6; i++)x=((double)(rand()%10)/10+x/10);
    return x;
}
void calculate(int l,int q,double t,double *sumh,double *sumh2,double *summ,double *summ2)
{
    int a[129][129],b[10];
    int i,j,x,y,at,count=0;
    double p,dh,dm;
    for(i=0; i<l; i++)
        for(j=0; j<l; j++)a[i][j]=rand()%q;
    while(1)
        {
            x=rand()%l;
            y=rand()%l;
            at=rand()%q;
            if(at!=a[x][y])
                {
                    dh=0;
                    dh+=(x!=0)?delta(a[x][y],a[x-1][y]):delta(a[x][y],a[l-1][y]);
                    dh-=(x!=0)?delta(at,a[x-1][y]):delta(at,a[l-1][y]);
                    dh+=(x!=(l-1))?delta(a[x][y],a[x+1][y]):delta(a[x][y],a[0][y]);
                    dh-=(x!=(l-1))?delta(at,a[x+1][y]):delta(at,a[0][y]);
                    dh+=(y!=0)?delta(a[x][y],a[x][y-1]):delta(a[x][y],a[x][l-1]);
//dh-=(y!=0)?delta(at,a[x+1][y]):delta(at,a[0][y]);//
                    dh-=(y!=0)?delta(at,a[x][y-1]):delta(at,a[x][l-1]);
                    dh+=(y!=(l-1))?delta(a[x][y],a[x][y+1]):delta(a[x][y],a[x][0]);
                    dh-=(y!=(l-1))?delta(at,a[x][y+1]):delta(at,a[x][0]);
                    p=random1();
                    if(p<exp(-dh/t)) a[x][y]=at;
                }
            else if(count<50000)
                {
                    count+=isMK(x,y);
                    if(count==50000)
                        {
                            (*sumh)=0;
                            (*sumh2)=0;
                            (*summ)=0;
                            (*summ2)=0;
                        }
                    continue;
                }
            count+=isMK(x,y);
            if(count>=50000&&1==isMK(x,y))
                {
                    if(count==50000)
                        {
                            (*sumh)=0;
                            (*sumh2)=0;
                            (*summ)=0;
                            (*summ2)=0;
                        }
                    dh=0;
                    dm=0;
                    for(i=0; i<q; i++)b[i]=0;
                    //for(x=rand()%4; x<l; x+=4)
                    for(x=0; x<l; x++)
                        {
                            //for(y=rand()%4; y<l; y+=4)
                            for(y=0; y<l; y++)
                                {
                                    dh-=(x!=0)?delta(a[x][y],a[x-1][y]):delta(a[x][y],a[l-1][y]);

                                    dh-=(x!=(l-1))?delta(a[x][y],a[x+1][y]):delta(a[x][y],a[0][y]);

                                    dh-=(y!=0)?delta(a[x][y],a[x][y-1]):delta(a[x][y],a[x][l-1]);

                                    dh-=(y!=(l-1))?delta(a[x][y],a[x][y+1]):delta(a[x][y],a[x][0]);
                                    b[a[x][y]]++;
                                }
                        }
                    for(i=1; i<q; i++)b[0]=(b[i]>b[0])?b[i]:b[0];
                    //dm=(16*(double)(b[0]*q)/(double)(l*l)-1)/(double)(q-1);
                    dm=((double)(b[0]*q)/(double)(l*l)-1)/(double)(q-1);
                    //double e=(16*dh/(double)(l*l));
                    double e=(dh/(double)(l*l));
                    e1[count]=e;
                    // (*sumh)+=(16*dh/(double)(l*l));
                    (*sumh)+=(dh/(double)(l*l));
                    // (*sumh2)+=(256*dh*dh)/(double)(l*l*l*l);
                    (*sumh2)+=(dh*dh)/(double)(l*l*l*l);
                    (*summ)+=dm;
                    (*summ2)+=dm*dm;
                }
            if(count>=100000)
                {
                    (*sumh)/=50000;
                    (*sumh2)/=50000;
                    (*summ)/=50000;
                    (*summ2)/=50000;
                    break;
                }
        }
}
