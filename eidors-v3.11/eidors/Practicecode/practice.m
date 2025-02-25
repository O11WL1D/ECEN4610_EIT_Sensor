% tutorial1_create_fwd_model
% $Id: tutorial020a.m 4092 2013-05-27 22:17:28Z bgrychtol $

r_mdl= eidors_obj('fwd_model','demo resistor model');
r_mdl = mdl_normalize( r_mdl, 0);

% Geometry
r_mdl.nodes= [1,1,1;  2,2,2];
r_mdl.elems= [1,2];
r_mdl.boundary= [1,2]; 

% Define Electrodes (there is only one)
r_mdl.electrode(1).z_contact= 10; % ohms
r_mdl.electrode(1).nodes=     1;
r_mdl.gnd_node= 2;

show_fem(r_mdl); view(-12,24);
print_convert tutorial020a.png '-density 50';














% Create stimulation patterns and solve fwd_model
% $Id: tutorial020b.m 3850 2013-04-16 18:13:39Z aadler $

% Define stimulation patterns
for i=1:3
    r_mdl.stimulation(i).stimulation= 'Amps';
    r_mdl.stimulation(i).stim_pattern= ( 0.001*i );
    r_mdl.stimulation(i).meas_pattern= 1; % measure electrode 1
end

r_mdl.solve=      @tutorial020_f_solve;

% Define an 'image'
resistor = eidors_obj('image', 'resistor');
resistor.elem_data= 1000;
resistor.fwd_model= r_mdl;

% Calculate data for 1k resistor
data_1k0 =fwd_solve( resistor );

% Now change resistor to be 1.2k
resistor.elem_data= 1200;
data_1k2 =fwd_solve( resistor );






% Solve resistor model
% $Id: tutorial020c.m 3127 2012-06-08 16:19:25Z bgrychtol $

% Now we complete the fwd_model
r_mdl.jacobian= @jacobian_perturb;

% Now create an inverse model
i_mdl= eidors_obj('inv_model','resistor inverse');
i_mdl.fwd_model= r_mdl;
i_mdl.jacobian_bkgnd.value= 1000;

% regulatization not needed for this problem
i_mdl.RtR_prior= @prior_tikhonov;
i_mdl.hyperparameter.value= 0;

i_mdl.reconst_type= 'difference';
i_mdl.solve= @inv_solve_diff_GN_one_step;

% Reconstruct resistor change
reconst= inv_solve(i_mdl, data_1k0, data_1k2);




% !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! BASIC CODE TESTING !!!!!!!!!!!!!!!!!!!



 disp(data_1k0)

 disp(data_1k0.meas')





%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IMAGE RECONSTRUCTION TEST!!!!!!!!!!!!!!!!!!!!

%bkgnd= 1;

%img= mk_image(resistor.fwd_model, bkgnd);
%vh= fwd_solve( img );

%show_fem(img,bkgnd);


% I guess the show fem function images a image type object,
% this is pulling errors for some reason 



















function data =tutorial020_f_solve( img )
% Forward Model for a resistor
% For each stimulation there is I1 into Node1
%  Node2 is connected to gnd with Zcontact
%
% each stim has one measurement pattern where
%  Vmeas= Meas_pat * Node1
%       = Meas_pat * I1 * ( Zcontact*2 + R )
%
% Thus
%  V= IR    => [V1;V2;V3] = [I1;I2*I3]*(R + 2*Zcontact)

  R= img.elem_data;
  stim = img.fwd_model.stimulation;

  n_stim= length( stim );
  V= zeros(n_stim, 1);

  for i=1:n_stim
    I        = stim(i).stim_pattern;
    meas_pat = stim(i).meas_pattern;

    zc       = img.fwd_model.electrode( find(I) ).z_contact;

    V(i)     = meas_pat * I * ( R + 2*zc);
  end

  data.name='resistor model data';
  data.meas= V;

end

