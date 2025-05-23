% Example of using EIDORS to simulate 2D data and to
% solve it using various 2D solvers
% (C) 2005 Andy Adler. License: GPL version 2 or version 3
% $Id: demo_2d_simdata.m 3125 2012-06-08 16:16:24Z bgrychtol $
% 
% Step 1: Create simple 16 electrode 2D model
% 
% get parameters for model from mk_circ_tank
% param= mk_circ_tank(rings, levels, n_elec, n_planes )
n_elec= 4;
n_rings= 1;
%options = {'no_meas_current','rotate_meas'};
 options = {'no_meas_current','no_rotate_meas'};
params= mk_circ_tank(12, [], n_elec ); 
params.stimulation= mk_stim_patterns(n_elec, n_rings, '{ad}','{ad}', ...
                            options, 10);
params.solve=      'fwd_solve_1st_order';
params.system_mat= 'system_mat_1st_order';
mdl_2d = eidors_obj('fwd_model', params);
%show_fem( mdl_2d ); % pause;
% create homogeneous image + simulate data
mat= ones( size(mdl_2d.elems,1) ,1);
homg_img= eidors_obj('image', 'homogeneous image', ...
                     'elem_data', mat, ...
                     'fwd_model', mdl_2d );
homg_data=fwd_solve( homg_img);
% create inhomogeneous image + simulate data
%mat([65,81,82,101,102,122])=2;


%mat([288])=2;

%mat([576])=2;
%mat([1])=2;
%mat([10])=2;


%mat([1:10])=2;

%mat([1])=2;
%mat([2])=2;
%mat([3])=2;
%mat([4])=2;

mat([576:400])=2;


L= length(mat)
disp(L)

inh_img= eidors_obj('image', 'homogeneous image', ...
                     'elem_data', mat, ...
                     'fwd_model', mdl_2d );
inh_data=fwd_solve( inh_img);
show_fem(inh_img)
