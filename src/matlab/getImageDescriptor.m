function hist = getImageDescriptor(model, descrs)

    descrs = single (descrs); 
    numWords = size(model.vocab, 2) ;

    % quantize local descriptors into visual words
    switch model.quantizer
      case 'vq'
        [drop, binsa] = min(vl_alldist(model.vocab, sdescrs), [], 1) ;
      case 'kdtree'
        binsa = double(vl_kdtreequery(model.kdtree, model.vocab, ...
                                      descrs, ...
                                      'MaxComparisons', 50)) ;
    end


       hists = zeros(numWords, 1) ;
       hists = vl_binsum(hists, ones(size(binsa)), binsa) ;
%        hists = single(hist / sum(hist)) ;

     hist = hists ;
     hist = hist / sum(hist) ;
end 