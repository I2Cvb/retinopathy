function m = removeinf(a, defaultval)
    
    if nargin == 1
	defaultval = 1;
    end
    
    valid = find(~isinf(a));
    
    m = repmat(defaultval, size(a));
    m(valid) = a(valid);