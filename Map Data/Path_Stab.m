M=dlmread('Copy of Mission1_Revised.csv',',',1,0);
lat = M(1:end,1);
long = M(1:end,2);

ipath = sqrt((abs(lat(end)-lat(1))).^2+(abs(long(end)-long(1)).^2));
vlat = advec(lat);
vlong = advec(long);
vres = zeros(size(vlat));

for ind = 1:length(lat)-1
    vres(ind) = sqrt((vlat(ind)).^2+(vlong(ind)).^2);
    
end
     
apath = sum(vres);
PS = ipath/apath;
disp(PS);
 