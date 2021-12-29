M1=dlmread('Final_Swarm1.csv',',',1,0);
M2=dlmread('Final_Swarm2.csv',',',1,0);
M3=dlmread('Final_Swarm3.csv',',',1,0);


lat1 = M1(1:end,1);
long1 = M1(1:end,2);
lat2 = M2(1:end,1);
long2 = M2(1:end,2);
lat3 = M3(1:end,1);
long3 = M3(1:end,2);

Lats = [length(lat1),length(lat2),length(lat3)];
fp = min(Lats);

for ind = 1:fp
    da12(ind) = 110570*(abs(lat1(ind)-lat2(ind))); 
    da13(ind) = 110570*(abs(lat1(ind)-lat3(ind)));
    da23(ind) = 110570*(abs(lat2(ind)-lat3(ind)));
    dn12(ind) = 93367.82*(abs(long1(ind)-long2(ind)));
    dn13(ind) = 93367.82*(abs(long1(ind)-long3(ind)));
    dn23(ind) = 93367.82*(abs(long2(ind)-long3(ind)));
end
    
for ind = 1:fp
    dr12(ind) = sqrt((da12(ind)).^2+(dn12(ind)).^2);
    dr13(ind) = sqrt((da13(ind)).^2+(dn13(ind)).^2);
    dr23(ind) = sqrt((da23(ind)).^2+(dn23(ind)).^2);
    
end

TD12 = sum(dr12);
TD13 = sum(dr13);
TD23 = sum(dr23);

ST12 = TD12/fp
ST13 = TD13/fp
ST23 = TD23/fp
    
    
        


    




