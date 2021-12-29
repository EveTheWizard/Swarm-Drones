%import data and separate columns
M=dlmread('Mission1_Revised.csv',',',1,0);
Ttot = M(end,3)-M(1,3);
lat = M(1:end,1);
long = M(1:end,2);
snom = 2*0.169164;


vlat = advec(lat);
vlong = advec(long);
vres = zeros(size(vlat));

%sum all path vectors and calculate magnitude
for ind = 1:length(lat)-1
    vres(ind) = sqrt((vlat(ind)).^2+(vlong(ind)).^2);
    
end

%calculate total path length, divide by total time
apath = sum(vres);
atime = apath/snom;

atd = abs(atime - Ttot);
disp(atd);
