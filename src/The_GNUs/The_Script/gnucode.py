
def get_gnuplot_code():

    gnucode=r'''
#set terminal epslatex size 15.11787cm,20cm standalone header "\\usepackage{amsmath,amstext,amssymb} \n \\usepackage[utf8]{inputenc} \n \\usepackage[outdir=./]{epstopdf} \n \
#\\renewcommand{\\bar}[1]{\\mkern 1.5mu\\overline{\\mkern-1.5mu#1\\mkern-1.5mu}\\mkern 1.5mu} \n \\graphicspath{{../}}  \n \\newcommand{\\upright}[1]{\\mathrm{#1}}" font ",11" 
    set terminal epslatex size 15.11787cm,20cm standalone header "\\usepackage{amsmath,amstext,amssymb} \n \\usepackage[utf8]{inputenc} \n \\usepackage[outdir=./]{epstopdf} \n \
    \\renewcommand{\\bar}[1]{\\mkern 1.5mu\\overline{\\mkern-1.5mu#1\\mkern-1.5mu}\\mkern 1.5mu} \n \\graphicspath{{../}}  \n \\newcommand{\\upright}[1]{\\mathsf{#1}} \n \
    \\renewcommand{\\familydefault}{\\sfdefault} \n \\usepackage{sfmath}" font ",11" linewidth 4 

#a10=a9=a8=a7=a6=a5=a4=a3=a2=a1=1.0
#b10=b9=b8=b7=b6=b5=b4=b3=b2=b1=-1.0
#c10=c9=c8=c7=c6=c5=c4=c3=c2=c1=0.1
#d10=d9=d8=d7=d6=d5=d4=d3=d2=d1=-1000.0

    a10=a9=a8=a7=a6=a5=a4=a3=a2=a1=100.0
    b10=b9=b8=b7=b6=b5=b4=b3=b2=b1=-1000.0
    c10=c9=c8=c7=c6=c5=c4=c3=c2=c1=10000.0
    d10=d9=d8=d7=d6=d5=d4=d3=d2=d1=-1000.0

# x5              = 0.0980358      
# y5              = 0.268468        
# a5              = 8.89385        
# b5              = -2318.88        
# c5              = 22077.4         

# x4              = 0.14063        
# y4              = 0.228367        
# a4              = 9.3508          
# b4              = -2566.99
# c4              = 29645.1           

# x3              = 0.213053         
# y3              = 0.186509     
# a3              = 10.4047       
# b3              = -6163.14      
# c3              = 135889              

# x2              = 0.366082     
# y2              = 0.257704        
# a2              = 9.95757        
# b2              = -2236.91  
# c2              = 11565.5           

# x1              = 0.69661       
# y1              = 0.266759       
# a1              = 13.8935        
# b1              = -10035.6     
# c1              = -131990               

    f10(x)=y10+a10*(x-x10)+b10*(x-x10)**3+c10*(x-x10)**4 #+ d10*(x-x10)**5
    f9(x)=y9+a9*(x-x9)+b9*(x-x9)**3+c9*(x-x9)**4 #+ d9*(x-x9)**5
    f8(x)=y8+a8*(x-x8)+b8*(x-x8)**3+c8*(x-x8)**4 #+ d8*(x-x8)**5
    f7(x)=y7+a7*(x-x7)+b7*(x-x7)**3+c7*(x-x7)**4 #+ d7*(x-x7)**5
    f6(x)=y6+a6*(x-x6)+b6*(x-x6)**3+c6*(x-x6)**4 #+ d6*(x-x6)**5
    f5(x)=y5+a5*(x-x5)+b5*(x-x5)**3+c5*(x-x5)**4 #+ d5*(x-x5)**5
    f4(x)=y4+a4*(x-x4)+b4*(x-x4)**3+c4*(x-x4)**4 #+ d4*(x-x4)**5
    f3(x)=y3+a3*(x-x3)+b3*(x-x3)**3+c3*(x-x3)**4 #+ d3*(x-x3)**5
    f2(x)=y2+a2*(x-x2)+b2*(x-x2)**3+c2*(x-x2)**4 #+ d2*(x-x2)**5
    f1(x)=y1+a1*(x-x1)+b1*(x-x1)**3+c1*(x-x1)**4 #+ d1*(x-x1)**5

    if (gf==1) {
    if (alt==1) {
        x10=0.05
        y10=0.1
        x9=0.05
        y9=0.1
        x8=0.05
        y8=0.1
        x7=0.05
        y7=0.1
        x6=0.05
        y6=0.1
        x5=0.1
        y5=0.1
        x4=0.15
        y4=0.1
        x3=0.2
        y3=0.1
        x2=0.3
        y2=0.1
        x1=0.6
        y1=0.1


        xl10=0.0					
        xr10=0.0735
        fit [xl10:xr10] f10(x) "../Data/D15.48/relvol.Nt24_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x10,y10,a10,b10,c10 #, d10
        redchisqr10=FIT_STDFIT**2

        xl9=0.0	
        xr9=0.0638				
        fit [xl9:xr9] f9(x) "../Data/D15.48/relvol.Nt20_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x9,y9,a9,b9,c9 #, d9
        redchisqr9=FIT_STDFIT**2
        
        xl8=0.0	
        xr8=0.0494	
        fit [xl8:xr8] f8(x) "../Data/D15.48/relvol.Nt18_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x8,y8,a8,b8,c8 #, d8
        redchisqr8=FIT_STDFIT**2
                        
        xl7=0.013									
        xr7=0.091	
        fit [xl7:xr7] f7(x) "../Data/D15.48/relvol.Nt16_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x7,y7,a7,b7,c7 #, d7
        redchisqr7=FIT_STDFIT**2
        
        xl6=0.0103							
        xr6=0.1236		
        fit [xl6:xr6] f6(x) "../Data/D15.48/relvol.Nt14_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x6,y6,a6,b6,c6 #, d6
        redchisqr6=FIT_STDFIT**2
        
        xl5=0.0684			
        xr5=0.1254								
        fit [xl5:xr5] f5(x) "../Data/D15.48/relvol.Nt12_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x5,y5,a5,b5,c5 #, d5
        redchisqr5=FIT_STDFIT**2

        xl4=0.1104				
        xr4=0.1872			
        fit [xl4:xr4] f4(x) "../Data/D15.48/relvol.Nt10_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x4,y4,a4,b4,c4 #, d4
        redchisqr4=FIT_STDFIT**2

        xl3=0.1845		
        xr3=0.2419		
        fit [xl3:xr3] f3(x) "../Data/D15.48/relvol.Nt8_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x3,y3,a3,b3,c3 #, d3
        redchisqr3=FIT_STDFIT**2

        xl2=0.3096							
        xr2=0.3528				
        fit [xl2:xr2] f2(x) "../Data/D15.48/relvol.Nt6_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x2,y2,a2,b2,c2 #, d2
        redchisqr2=FIT_STDFIT**2

        xl1=0.5635			
        xr1=0.588
        fit [xl1:xr1] f1(x) "../Data/D15.48/relvol.Nt4_t1.500000_ALTERNATING" using 1:2:3:4 xyerrors via x1,y1,a1,b1,c1 #, d1
        redchisqr1=FIT_STDFIT**2
    }
    else {

        x10=0.05
        y10=0.1
        x9=0.05
        y9=0.1
        x8=0.05
        y8=0.1
        x7=0.05
        y7=0.1
        x6=0.05
        y6=0.1
        x5=0.1
        y5=0.1
        x4=0.15
        y4=0.1
        x3=0.2
        y3=0.1
        x2=0.3
        y2=0.1
        x1=0.6
        y1=0.1


        xl10=0.0					
        xr10=0.0837
        #xr10=0.0432
        fit [xl10:xr10] f10(x) "../Data/D15.48/relvol.Nt24_t1.500000" using 1:2:3:4 xyerrors via x10,y10,a10,b10,c10 #, d10
        redchisqr10=FIT_STDFIT**2

        xl9=0.0	
        xr9=0.0561				
        #xr9=0.0396
        fit [xl9:xr9] f9(x) "../Data/D15.48/relvol.Nt20_t1.500000" using 1:2:3:4 xyerrors via x9,y9,a9,b9,c9 #, d9
        redchisqr9=FIT_STDFIT**2
        
        xl8=0.0	
        #xr8=0.081	
        xr8=0.0784	
        fit [xl8:xr8] f8(x) "../Data/D15.48/relvol.Nt18_t1.500000" using 1:2:3:4 xyerrors via x8,y8,a8,b8,c8 #, d8
        redchisqr8=FIT_STDFIT**2

        #xl7=0.0088	
        #xr7=0.066					
        xl7=0.0176						
        xr7=0.0792	
        fit [xl7:xr7] f7(x) "../Data/D15.48/relvol.Nt16_t1.500000" using 1:2:3:4 xyerrors via x7,y7,a7,b7,c7 #, d7
        redchisqr7=FIT_STDFIT**2
        
        #xl6=0.0321		
        #xr6=0.1177	
        xl6=0.048					
        xr6=0.114	
        fit [xl6:xr6] f6(x) "../Data/D15.48/relvol.Nt14_t1.500000" using 1:2:3:4 xyerrors via x6,y6,a6,b6,c6 #, d6
        redchisqr6=FIT_STDFIT**2
        
        xl5=0.0744	
        xr5=0.1178
        #xl5=0.062		
        #xr5=0.1085									
        fit [xl5:xr5] f5(x) "../Data/D15.48/relvol.Nt12_t1.500000" using 1:2:3:4 xyerrors via x5,y5,a5,b5,c5 #, d5
        redchisqr5=FIT_STDFIT**2

        xl4=0.119		
        xr4=0.1768	
        #xl4=0.1102		
        #xr4=0.1566			
        fit [xl4:xr4] f4(x) "../Data/D15.48/relvol.Nt10_t1.500000" using 1:2:3:4 xyerrors via x4,y4,a4,b4,c4 #, d4
        redchisqr4=FIT_STDFIT**2

        xl3=0.182	
        xr3=0.2262
        #xl3=0.1768			
        #xr3=0.221			
        fit [xl3:xr3] f3(x) "../Data/D15.48/relvol.Nt8_t1.500000" using 1:2:3:4 xyerrors via x3,y3,a3,b3,c3 #, d3
        redchisqr3=FIT_STDFIT**2

        xl2=0.3132			
        #xl2=0.3103		
        xr2=0.3393		
        fit [xl2:xr2] f2(x) "../Data/D15.48/relvol.Nt6_t1.500000" using 1:2:3:4 xyerrors via x2,y2,a2,b2,c2 #, d2
        redchisqr2=FIT_STDFIT**2

        xl1=0.565		
        xr1=0.585
        fit [xl1:xr1] f1(x) "../Data/D15.48/relvol.Nt4_t1.500000" using 1:2:3:4 xyerrors via x1,y1,a1,b1,c1 #, d1
        redchisqr1=FIT_STDFIT**2

    }
    }
    else {
    if (alt==1) {
        x10=0.05
        y10=0.1
        x9=0.05
        y9=0.1
        x8=0.05
        y8=0.1
        x7=0.05
        y7=0.1
        x6=0.05
        y6=0.1
        x5=0.1
        y5=0.1
        x4=0.15
        y4=0.1
        x3=0.2
        y3=0.1
        #x2=0.4
        x2=0.35
        y2=0.1
        x1=0.7
        y1=0.1


        xl10=0.0					
        xr10=0.0688
        fit [xl10:xr10] f10(x) "../Data/D15.48/relvol.Nt24_ALTERNATING" using 1:2:3:4 xyerrors via x10,y10,a10,b10,c10 #, d10
        redchisqr10=FIT_STDFIT**2

        xl9=0.0	
        xr9=0.0666
        #xr9=0.0592
        fit [xl9:xr9] f9(x) "../Data/D15.48/relvol.Nt20_ALTERNATING" using 1:2:3:4 xyerrors via x9,y9,a9,b9,c9 #, d9
        redchisqr9=FIT_STDFIT**2

        xl8=0.0	
        xr8=0.0949				
        #xr8=0.1125	
        fit [xl8:xr8] f8(x) "../Data/D15.48/relvol.Nt18_ALTERNATING" using 1:2:3:4 xyerrors via x8,y8,a8,b8,c8 #, d8
        redchisqr8=FIT_STDFIT**2

        xl7=0.0082	
        xr7=0.1148
        #xl7=0.0	
        #xr7=0.0747
        fit [xl7:xr7] f7(x) "../Data/D15.48/relvol.Nt16_ALTERNATING" using 1:2:3:4 xyerrors via x7,y7,a7,b7,c7 #, d7
        redchisqr7=FIT_STDFIT**2

        xl6=0.0109								
        xr6=0.1308
        #xl6=0.0218	
        #xr6=0.1308
        ##xl6=0.0	
        ##xr6=0.0904
        fit [xl6:xr6] f6(x) "../Data/D15.48/relvol.Nt14_ALTERNATING" using 1:2:3:4 xyerrors via x6,y6,a6,b6,c6 #, d6
        redchisqr6=FIT_STDFIT**2

        ##xl5=0.0798		
        ##xr5=0.171	
        xl5=0.0623			
        xr5=0.1424
        #xl5=0.0534										
        #xr5=0.1424	
        fit [xl5:xr5] f5(x) "../Data/D15.48/relvol.Nt12_ALTERNATING" using 1:2:3:4 xyerrors via x5,y5,a5,b5,c5 #, d5
        redchisqr5=FIT_STDFIT**2
        
        ##xl4=0.111		
        ##xr4=0.162
        xl4=0.121		
        xr4=0.187
        #xl4=0.1134			
        #xr4=0.189
        #xl4=0.117	
        #xr4=0.1872
        fit [xl4:xr4] f4(x) "../Data/D15.48/relvol.Nt10_ALTERNATING" using 1:2:3:4 xyerrors via x4,y4,a4,b4,c4 #, d4
        redchisqr4=FIT_STDFIT**2

        ##xl3=0.2072		
        ##xr3=0.2479		
        xl3=0.1804			
        xr3=0.2665	
        #xl3=0.1825					
        #xr3=0.2774	
        fit [xl3:xr3] f3(x) "../Data/D15.48/relvol.Nt8_ALTERNATING" using 1:2:3:4 xyerrors via x3,y3,a3,b3,c3 #, d3
        redchisqr3=FIT_STDFIT**2

        ##xl2=0.3075	
        ##xr2=0.39
        xl2=0.3172				
        xr2=0.4026
        #xl2=0.3172		
        #xr2=0.4148
        ##xl2=0.3321			
        ##xr2=0.4182	
        ##xl2=0.3198	
        ##xr2=0.4059
        fit [xl2:xr2] f2(x) "../Data/D15.48/relvol.Nt6_ALTERNATING" using 1:2:3:4 xyerrors via x2,y2,a2,b2,c2 #, d2
        redchisqr2=FIT_STDFIT**2

        ##xl1=0.6875	
        ##xr1=0.7225
        xl1=0.6612						
        xr1=0.7308
        #xl1=0.6728	
        #xr1=0.7424
        ##xl1=0.68			
        ##xr1=0.728
        fit [xl1:xr1] f1(x) "../Data/D15.48/relvol.Nt4_ALTERNATING" using 1:2:3:4 xyerrors via x1,y1,a1,b1,c1 #, d1
        redchisqr1=FIT_STDFIT**2
    }
    else {
        x10=0.05
        y10=0.1
        x9=0.05
        y9=0.1
        x8=0.05
        y8=0.1
        x7=0.05
        y7=0.1
        x6=0.05
        y6=0.1
        x5=0.1
        y5=0.1
        x4=0.15
        y4=0.1
        x3=0.2
        y3=0.1
        #x2=0.4
        x2=0.35
        y2=0.1
        x1=0.7
        y1=0.1


        xl10=0.0					
        xr10=0.0621
        fit [xl10:xr10] f10(x) "../Data/D15.48/relvol.Nt24" using 1:2:3:4 xyerrors via x10,y10,a10,b10,c10 #, d10
        redchisqr10=FIT_STDFIT**2

        xl9=0.0	
        xr9=0.0464
        fit [xl9:xr9] f9(x) "../Data/D15.48/relvol.Nt20" using 1:2:3:4 xyerrors via x9,y9,a9,b9,c9 #, d9
        redchisqr9=FIT_STDFIT**2

        xl8=0.0087			
        xr8=0.0667
        #xl8=0.004			
        #xr8=0.076
        #xl8=0.0144	
        #xr8=0.0648
        fit [xl8:xr8] f8(x) "../Data/D15.48/relvol.Nt18" using 1:2:3:4 xyerrors via x8,y8,a8,b8,c8 #, d8
        redchisqr8=FIT_STDFIT**2

        xl7=0.0172			
        xr7=0.0774	
        fit [xl7:xr7] f7(x) "../Data/D15.48/relvol.Nt16" using 1:2:3:4 xyerrors via x7,y7,a7,b7,c7 #, d7
        redchisqr7=FIT_STDFIT**2

        xl6=0.0365		
        xr6=0.0876
        #xl6=0.025				
        #xr6=0.1	
        xl6=0.0248				
        xr6=0.1116										
        fit [xl6:xr6] f6(x) "../Data/D15.48/relvol.Nt14" using 1:2:3:4 xyerrors via x6,y6,a6,b6,c6 #, d6
        redchisqr6=FIT_STDFIT**2

        #xl5=0.0598		
        #xr5=0.1196			
        xl5=0.0672	
        xr5=0.1632				
        #xl5=0.061		
        #xr5=0.1586
        #xl5=0.0549	
        #xr5=0.1464						
        fit [xl5:xr5] f5(x) "../Data/D15.48/relvol.Nt12" using 1:2:3:4 xyerrors via x5,y5,a5,b5,c5 #, d5
        redchisqr5=FIT_STDFIT**2

        xl4=0.1155	
        xr4=0.1815			
        #xl4=0.1144	
        #xr4=0.1872
        #xl4=0.0966	
        #xr4=0.1702			
        #xl4=0.1066	
        #xr4=0.1638
        fit [xl4:xr4] f4(x) "../Data/D15.48/relvol.Nt10" using 1:2:3:4 xyerrors via x4,y4,a4,b4,c4 #, d4
        redchisqr4=FIT_STDFIT**2

        xl3=0.19	
        xr3=0.2432		
        fit [xl3:xr3] f3(x) "../Data/D15.48/relvol.Nt8" using 1:2:3:4 xyerrors via x3,y3,a3,b3,c3 #, d3
        redchisqr3=FIT_STDFIT**2

        xl2=0.3298	
        xr2=0.4046		
        fit [xl2:xr2] f2(x) "../Data/D15.48/relvol.Nt6" using 1:2:3:4 xyerrors via x2,y2,a2,b2,c2 #, d2
        redchisqr2=FIT_STDFIT**2

        xl1=0.66	
        xr1=0.7128
        #xl1=0.6776	
        #xr1=0.7238
        fit [xl1:xr1] f1(x) "../Data/D15.48/relvol.Nt4" using 1:2:3:4 xyerrors via x1,y1,a1,b1,c1 #, d1
        redchisqr1=FIT_STDFIT**2
    }
    }

    set print "D15.48_me_NEW"
    print "N_t\tl_c\t\ts(l_c)"

    print sprintf("24\t%.9g\t%.9g",x10,x10_err)
    print sprintf("20\t%.9g\t%.9g",x9,x9_err)
    print sprintf("18\t%.9g\t%.9g",x8,x8_err)
    print sprintf("16\t%.9g\t%.9g",x7,x7_err)
    print sprintf("14\t%.9g\t%.9g",x6,x6_err)
    print sprintf("12\t%.9g\t%.9g",x5,x5_err)
    print sprintf("10\t%.9g\t%.9g",x4,x4_err)
    print sprintf("8\t%.9g\t%.9g",x3,x3_err)
    print sprintf("6\t%.9g\t%.9g",x2,x2_err)
    print sprintf("4\t%.9g\t%.9g",x1,x1_err)

    unset print 

    set cbrange[1.0:8.0]
    set palette defined (-1 "#0000AA", 1 "#AA0000")
    unset colorbox

    unset ylabel
#set xrange[-75.0:3750.0]
    set xrange[-100.0:3650.0]

    scaling_factor=1.4
#a=0.0646/197.327
#a_err=0.0007/197.327
    a=0.0619/197.327
    a_err=0.0018/197.327

    set output "Plots/D15.48_pr_NEW.tex"

    set multiplot layout 10,1 margins screen 0.105, 0.99, 0.06, 0.97 spacing screen 0.0
#set multiplot layout 10,1 margins screen 0.085, 0.995, 0.05, 0.97 spacing screen 0.0

#set label '\Large $L=3.10(3)\,\upright{fm}$' at graph 0.5,screen 0.985 center
#set label '\Large D210: $a=0.0646(7)\,\upright{fm}$, $m_\pi=213(9)\,\upright{MeV}$, $L=3.10(3)\,\upright{fm}$' at graph 0.5,screen 0.985 center 
    set label '\normalsize D210: $a=0.0619(18)\,\upright{fm}$, $m_\pi=225(7)\,\upright{MeV}$, $L=2.97(9)\,\upright{fm}$' at graph 0.5,screen 0.985 center

    OFFSET=scaling_factor*50.0

    LINECOLOR=1
    POINTTYPE=1

    set format x ''
    unset xlabel

    set yrange[0:1]
    set ytics 0,0.2,1.0
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0 
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt24_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt24_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt24_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt24"}} 
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 1.0000 notitle
    unset arrow 1
    unset label
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl10/a,graph 0 to scaling_factor*xl10/a,graph 1 nohead lc "red" 
    set arrow 3 from scaling_factor*xr10/a,graph 0 to scaling_factor*xr10/a,graph 1 nohead lc "red" 
    plot sample [t=scaling_factor*xl10/a-OFFSET:scaling_factor*xr10/a+OFFSET] f10(t*a/scaling_factor) lc LINECOLOR notitle
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.7, graph 0.9 
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(24*a),a_err/(24*a*a)), "+" u (scaling_factor*x10/a):(f10(x10)):(scaling_factor*sqrt((x10_err/a)**2+(x10*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x10/a,scaling_factor*sqrt((x10_err/a)**2+(x10*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(24*a),a_err/(24*a*a)), "+" u (scaling_factor*x10/a):(f10(x10)):(scaling_factor*x10_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x10/a,scaling_factor*x10_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.986, graph 0.85 box height +3.25 width -50.5 opaque
    set key at graph 0.986, graph 0.9  box height +2.9 width -50.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr10,scaling_factor*binsize10/a,scaling_factor*xl10/a,scaling_factor*xr10/a)

    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0 
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt20_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt20_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt20_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt20"}} 
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 1.2000 notitle
    unset arrow 1
    unset label
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl9/a,graph 0 to scaling_factor*xl9/a,graph 1 nohead lc "red" 
    set arrow 3 from scaling_factor*xr9/a,graph 0 to scaling_factor*xr9/a,graph 1 nohead lc "red" 
    plot sample [t=scaling_factor*xl9/a-OFFSET:scaling_factor*xr9/a+OFFSET] f9(t*a/scaling_factor) lc LINECOLOR notitle
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.7, graph 0.9 
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.2000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(20*a),a_err/(20*a*a)), "+" u (scaling_factor*x9/a):(f9(x9)):(scaling_factor*sqrt((x9_err/a)**2+(x9*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x9/a,scaling_factor*sqrt((x9_err/a)**2+(x9*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.2000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(20*a),a_err/(20*a*a)), "+" u (scaling_factor*x9/a):(f9(x9)):(scaling_factor*x9_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x9/a,scaling_factor*x9_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.986, graph 0.85 box height +3.25 width -50.5 opaque
    set key at graph 0.986, graph 0.9  box height +2.9 width -50.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr9,scaling_factor*binsize9/a,scaling_factor*xl9/a,scaling_factor*xr9/a)

#set yrange[0:1]
#set ytics 0,0.2,1.0
    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0 
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt18_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt18_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt18_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt18"}}
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 1.3333 notitle
    unset arrow 1
    unset label
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl8/a,graph 0 to scaling_factor*xl8/a,graph 1 nohead lc "red" 
    set arrow 3 from scaling_factor*xr8/a,graph 0 to scaling_factor*xr8/a,graph 1 nohead lc "red" 
    plot sample [t=scaling_factor*xl8/a-OFFSET:scaling_factor*xr8/a+OFFSET] f8(t*a/scaling_factor) lc LINECOLOR notitle
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.7, graph 0.9 
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.3333 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(18*a),a_err/(18*a*a)), "+" u (scaling_factor*x8/a):(f8(x8)):(scaling_factor*sqrt((x8_err/a)**2+(x8*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x8/a,scaling_factor*sqrt((x8_err/a)**2+(x8*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.3333 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(18*a),a_err/(18*a*a)), "+" u (scaling_factor*x8/a):(f8(x8)):(scaling_factor*x8_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x8/a,scaling_factor*x8_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.986, graph 0.85 box height +3.25 width -50.5 opaque
    set key at graph 0.986, graph 0.9  box height +2.9 width -51.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr8,scaling_factor*binsize8/a,scaling_factor*xl8/a,scaling_factor*xr8/a)

    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0 
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt16_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt16_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt16_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt16"}} 
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 1.5000 notitle
    unset arrow 1
    unset label
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl7/a,graph 0 to scaling_factor*xl7/a,graph 1 nohead lc "red" 
    set arrow 3 from scaling_factor*xr7/a,graph 0 to scaling_factor*xr7/a,graph 1 nohead lc "red" 
    plot sample [t=scaling_factor*xl7/a-OFFSET:scaling_factor*xr7/a+OFFSET] f7(t*a/scaling_factor) lc LINECOLOR notitle
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.7, graph 0.9 
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.5000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(16*a),a_err/(16*a*a)), "+" u (scaling_factor*x7/a):(f7(x7)):(scaling_factor*sqrt((x7_err/a)**2+(x7*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x7/a,scaling_factor*sqrt((x7_err/a)**2+(x7*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.5000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(16*a),a_err/(16*a*a)), "+" u (scaling_factor*x7/a):(f7(x7)):(scaling_factor*x7_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x7/a,scaling_factor*x7_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.986, graph 0.85 box height +3.25 width -51.5 opaque
    set key at graph 0.986, graph 0.9  box height +2.9 width -51.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr7,scaling_factor*binsize7/a,scaling_factor*xl7/a,scaling_factor*xr7/a)

    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0 
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt14_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt14_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt14_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt14"}}
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 1.7143 notitle
    unset arrow 1
    unset label
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl6/a,graph 0 to scaling_factor*xl6/a,graph 1 nohead lc "red" 
    set arrow 3 from scaling_factor*xr6/a,graph 0 to scaling_factor*xr6/a,graph 1 nohead lc "red" 
    plot sample [t=scaling_factor*xl6/a-OFFSET:scaling_factor*xr6/a+OFFSET] f6(t*a/scaling_factor) lc LINECOLOR notitle
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.7, graph 0.9 
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.7143 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(14*a),a_err/(14*a*a)), "+" u (scaling_factor*x6/a):(f6(x6)):(scaling_factor*sqrt((x6_err/a)**2+(x6*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x6/a,scaling_factor*sqrt((x6_err/a)**2+(x6*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 1.7143 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(14*a),a_err/(14*a*a)), "+" u (scaling_factor*x6/a):(f6(x6)):(scaling_factor*x6_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x6/a,scaling_factor*x6_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.986, graph 0.85 box height +3.25 width -51.5 opaque
    set key at graph 0.986, graph 0.9  box height +2.9 width -52.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr6,scaling_factor*binsize6/a,scaling_factor*xl6/a,scaling_factor*xr6/a)

    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0 
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt12_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt12_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt12_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt12"}} 
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 2.0000 notitle
    unset arrow 1
    unset label
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl5/a,graph 0 to scaling_factor*xl5/a,graph 1 nohead lc "red" 
    set arrow 3 from scaling_factor*xr5/a,graph 0 to scaling_factor*xr5/a,graph 1 nohead lc "red" 
    plot sample [t=scaling_factor*xl5/a-OFFSET:scaling_factor*xr5/a+OFFSET] f5(t*a/scaling_factor) lc LINECOLOR notitle
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.7, graph 0.9 
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 2.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(12*a),a_err/(12*a*a)), "+" u (scaling_factor*x5/a):(f5(x5)):(scaling_factor*sqrt((x5_err/a)**2+(x5*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x5/a,scaling_factor*sqrt((x5_err/a)**2+(x5*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 2.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(12*a),a_err/(12*a*a)), "+" u (scaling_factor*x5/a):(f5(x5)):(scaling_factor*x5_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x5/a,scaling_factor*x5_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.986, graph 0.85 box height +3.25 width -52.5 opaque
    set key at graph 0.986, graph 0.9  box height +2.9 width -52.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr5,scaling_factor*binsize5/a,scaling_factor*xl5/a,scaling_factor*xr5/a)

    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0  
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt10_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt10_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt10_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt10"}}
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 2.4000 notitle 
    unset arrow 1
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl4/a,graph 0 to scaling_factor*xl4/a,graph 1 nohead lc "red"  
    set arrow 3 from scaling_factor*xr4/a,graph 0 to scaling_factor*xr4/a,graph 1 nohead lc "red"
    plot sample [t=scaling_factor*xl4/a-OFFSET:scaling_factor*xr4/a+OFFSET] f4(t*a/scaling_factor) lc LINECOLOR notitle 
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.7, graph 0.9 
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 2.4000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(10*a),a_err/(10*a*a)), "+" u (scaling_factor*x4/a):(f4(x4)):(scaling_factor*sqrt((x4_err/a)**2+(x4*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x4/a,scaling_factor*sqrt((x4_err/a)**2+(x4*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 2.4000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(10*a),a_err/(10*a*a)), "+" u (scaling_factor*x4/a):(f4(x4)):(scaling_factor*x4_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x4/a,scaling_factor*x4_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.986, graph 0.85 box height +3.25 width -52.5 opaque
    set key at graph 0.986, graph 0.9  box height +2.9 width -52.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr4,scaling_factor*binsize4/a,scaling_factor*xl4/a,scaling_factor*xr4/a)

    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0 
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt8_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt8_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt8_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt8"}}
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 3.0000 notitle 
    unset arrow 1
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl3/a,graph 0 to scaling_factor*xl3/a,graph 1 nohead lc "red"  
    set arrow 3 from scaling_factor*xr3/a,graph 0 to scaling_factor*xr3/a,graph 1 nohead lc "red"
    plot sample [t=scaling_factor*xl3/a-OFFSET:scaling_factor*xr3/a+OFFSET] f3(t*a/scaling_factor) lc LINECOLOR notitle
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.7, graph 0.9
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 3.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(8*a),a_err/(8*a*a)), "+" u (scaling_factor*x3/a):(f3(x3)):(scaling_factor*sqrt((x3_err/a)**2+(x3*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x3/a,scaling_factor*sqrt((x3_err/a)**2+(x3*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 3.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(8*a),a_err/(8*a*a)), "+" u (scaling_factor*x3/a):(f3(x3)):(scaling_factor*x3_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x3/a,scaling_factor*x3_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.986, graph 0.85 box height +3.25 width -53.5 opaque
    set key at graph 0.986, graph 0.9 box height +2.9 width -53.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr3,scaling_factor*binsize3/a,scaling_factor*xl3/a,scaling_factor*xr3/a) 

    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0  
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt6_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt6_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt6_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt6"}}
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 4.0000 notitle
    unset arrow 1
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl2/a,graph 0 to scaling_factor*xl2/a,graph 1 nohead lc "red"  
    set arrow 3 from scaling_factor*xr2/a,graph 0 to scaling_factor*xr2/a,graph 1 nohead lc "red"
    plot sample [t=scaling_factor*xl2/a-OFFSET:scaling_factor*xr2/a+OFFSET] f2(t*a/scaling_factor) lc LINECOLOR notitle 
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.775, graph 0.85
    set key at graph 0.025, graph 0.9  
    set key left width -6.0
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 4.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(6*a),a_err/(6*a*a)), "+" u (scaling_factor*x2/a):(f2(x2)):(scaling_factor*sqrt((x2_err/a)**2+(x2*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x2/a,scaling_factor*sqrt((x2_err/a)**2+(x2*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 4.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(6*a),a_err/(6*a*a)), "+" u (scaling_factor*x2/a):(f2(x2)):(scaling_factor*x2_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x2/a,scaling_factor*x2_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
    set key default
#set key at graph 0.986, graph 0.85 box height +3.25 width -54.5 opaque
    set key at graph 0.986, graph 0.9  box height +2.9 width -54.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr2,scaling_factor*binsize2/a,scaling_factor*xl2/a,scaling_factor*xr2/a) 

    set format x 
    set xlabel '\normalsize $\lambda$ in $\upright{MeV}$'
    set ytics 0,0.2,0.8
    set key default
    set arrow 1 from 0,graph 0 to 0,graph 1 nohead dt 0  
    if (gf==1) {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt4_t1.500000_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt4_t1.500000"}} 
    else {if (alt==1) {relvol_file = "../Data/D15.48/relvol.Nt4_ALTERNATING"} else {relvol_file = "../Data/D15.48/relvol.Nt4"}} 
    plot relvol_file using (scaling_factor*$1/a):2:(scaling_factor*$3/a):4 with xyerrorbars pt POINTTYPE lc palette cb 6.0000 notitle
    unset arrow 1
    unset xlabel
    unset xtics
    unset ytics
    set multiplot previous
    set arrow 2 from scaling_factor*xl1/a,graph 0 to scaling_factor*xl1/a,graph 1 nohead lc "red"  
    set arrow 3 from scaling_factor*xr1/a,graph 0 to scaling_factor*xr1/a,graph 1 nohead lc "red"
    plot sample [t=scaling_factor*xl1/a-OFFSET:scaling_factor*xr1/a+OFFSET] f1(t*a/scaling_factor) lc LINECOLOR notitle
    unset arrow 2
    unset arrow 3
    set multiplot previous
#set key at graph 0.225, graph 0.85
    set key at graph 0.025, graph 0.9  
    set key left width -6.0
#plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 6.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(4*a),a_err/(4*a*a)), "+" u (scaling_factor*x1/a):(f1(x1)):(scaling_factor*sqrt((x1_err/a)**2+(x1*a_err/a**2)**2)) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x1/a,scaling_factor*sqrt((x1_err/a)**2+(x1*a_err/a**2)**2)) lw 1.5 ps 1.5 pt 6 lc "red"
    plot "+" u (1/0):(1/0):(1/0):(1/0) with xyerrorbars pt POINTTYPE lc palette cb 6.0000 title sprintf('\footnotesize$T=%.0f(%.0f)\,\upright{MeV}$',1/(4*a),a_err/(4*a*a)), "+" u (scaling_factor*x1/a):(f1(x1)):(scaling_factor*x1_err/a) with xerrorbars title sprintf('\footnotesize$\lambda_\upright{c}=%.0f(%.0f)\,\upright{MeV}$',scaling_factor*x1/a,scaling_factor*x1_err/a) lw 1.5 ps 1.5 pt 6 lc "red"
    set multiplot previous
#set key at graph 0.034, graph 0.85 box height +3.25 width -54.5 opaque 
#set key at graph 0.295, graph 0.85 box height +3.25 width -52.5 opaque
    set key at graph 0.345, graph 0.9  box height +2.9 width -54.0 opaque
    plot 1/0 lc LINECOLOR title sprintf('\scriptsize\shortstack[r]{$\chi^2/\upright{d.o.f.}=%.2f$\\$\Delta\lambda=%.1f\,\upright{MeV}$\\$\lambda_\upright{l}=%.0f\,\upright{MeV}$\\$\lambda_\upright{r}=%.0f\,\upright{MeV}$}',redchisqr1,scaling_factor*binsize1/a,scaling_factor*xl1/a,scaling_factor*xr1/a) 

    unset multiplot

    set multiplot layout 9,1 margins screen 0.105, 0.99, 0.06, 0.97 spacing screen 0.0
#set multiplot layout 9,1 margins screen 0.085, 0.995, 0.05, 0.97 spacing screen 0.0
    set yrange [0:1]
    unset arrow
    unset xlabel
    unset xtics
    unset ytics  
    plot 1/0 notitle
    plot 1/0 notitle
    plot 1/0 notitle
    plot 1/0 notitle
    set ylabel '\normalsize $r(\lambda)$' offset -3,0
    plot 1/0 notitle
    unset ylabel
    unset multiplot

    unset output
    '''

    return gnucode
