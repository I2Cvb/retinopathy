function mapping = getmapping(samples,mappingtype)
% Version 0.1.1
% Authors: Marko Heikkilä and Timo Ahonen

% Changelog
% 0.1.1 Changed output to be a structure
% Fixed a bug causing out of memory errors when generating rotation 
% invariant mappings with high number of sampling points.
% Lauge Sorensen is acknowledged for spotting this problem.



table = 0:2^samples-1;
newMax  = 0; %number of patterns in the resulting LBP code
index   = 0;

if strcmp(mappingtype,'u2') %Uniform 2
  newMax = samples*(samples-1) + 3; 
  table(1)= newMax-3;
  table(2^samples)=newMax-2;
  for i = 1:2^samples-2
    j = bitset(bitshift(i,1,samples),1,bitget(i,samples)); %rotate left
    numt = sum(bitget(bitxor(i,j),1:samples)); %number of 1->0 and
                                               %0->1 transitions
                                               %in binary string 
                                               %x is equal to the
                                               %number of 1-bits in
                                               %XOR(x,Rotate left(x)) 

    if numt == 2
        f1=find(bitget(bitand(i,bitcmp(j,samples)),1:samples));
        n=sum(bitget(i,1:samples));
        index = (n-1)*samples + mod( floor(n/2)+f1 , samples); 
        table(i+1) = index;
    else
      table(i+1) = newMax - 1;
    end
  end

  orbits=cell(samples+2,1);
  for i=1:samples-1
      orbits{i}=((i-1)*samples):(i*samples-1);
  end
  orbits{samples}=newMax-3;
  orbits{samples+1}=newMax-2;
  orbits{samples+2}=newMax-1;
else
    newMax=2^samples;
    found=false(newMax,1);
    orbits={};
    for i=0:newMax-1
        if(found(i+1)==false)
            found(i+1)=true;
            neworbit=i; 
            j=bitset(bitshift(i,1,samples),1,bitget(i,samples)); %rotate left
            while(j ~= i)
                neworbit=[neworbit j];
                found(j+1)=true;
                j=bitset(bitshift(j,1,samples),1,bitget(j,samples));
            end
            orbits{length(orbits)+1}=neworbit;
        end
    end
end


    

mapping.table=table;
mapping.samples=samples;
mapping.num=newMax;
mapping.orbits=orbits;