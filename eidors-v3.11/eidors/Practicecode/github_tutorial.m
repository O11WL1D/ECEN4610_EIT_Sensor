figure(1);

% create model
model = mk_common_model('e2c', 8);
img = mk_image(model);
img_prior = img;

% solve forward problem homogeneous
vh = fwd_solve(img);

img.elem_data([201, 229, 230, 261, 262, 294]) = 2;

% show model
show_fem(img);
axis square; axis off

% solve forward problem inhomogeneous
% for i = 1:40
    vi = fwd_solve(img);
%     vi.meas(i) = 2;
%     vi.meas(21) = 2;
    % Create Inverse Model
    inv2d= eidors_obj('inv_model', 'EIT inverse');
    inv2d.reconst_type= 'difference';
    inv2d.jacobian_bkgnd.value= 1;

    inv2d.fwd_model= model.fwd_model;

    % Guass-Newton solvers
    inv2d.solve=       @inv_solve_diff_GN_one_step;

    % Tikhonov prior
    inv2d.hyperparameter.value = .03;
    inv2d.RtR_prior=   @prior_tikhonov;
    imgr(1)= inv_solve( inv2d, vh, vi);
    figure(2);
    show_slices(imgr, [inf,inf,0,1,1]);
    title(num2str(i));
    pause(1);
% end

% % Create Inverse Model
% inv2d = eidors_obj('inv_model', '2D inverse', ...
%     'RtR_prior', img_prior, 'reconst_type', 'difference', ...
% 	'fwd_model', model.fwd_model, 'solve', 'inv_solve_diff_GN_one_step');
% inv2d.jacobian_bkgnd.value= 1;
% 
% % solve inverse problem
% imgr5= inv_solve( inv2d, vh, vi);




% % solve forward problem
% img= mk_image(imb.fwd_model,1);
% show_fem(img);
% rec_img= inv_solve(imdl_3d, homg_data, inh_data);
% 
% %%
% img = mk_image(imb.fwd_model, bkgnd);
% vh = fwd_solve( img );
% 
% img.elem_data([1,37,49:50,65:66,81:83,101:103,121:124])=bkgnd * 2;
% img.elem_data([95,98:100,79,80,76,63,64,60,48,45,36,33,22])=bkgnd * 2;
% vi= fwd_solve( img );
% 
% % Add -12dB SNR
% vi_n= vi; 
% nampl= std(vi.meas - vh.meas)*10^(-18/20);
% vi_n.meas = vi.meas + nampl *randn(size(vi.meas));
% 

%From <https://gist.github.com/SCBuergel/517611f56b22ccde1a22> 
