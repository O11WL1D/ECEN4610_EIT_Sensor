% Forward solvers $Id: forward_solvers01.m 3790 2013-04-04 15:41:27Z aadler $

% 2D Model
imdl= mk_common_model('a2d1c',19);

% Create an homogeneous image
img_1 = mk_image(imdl);
h1= subplot(221);
%show_fem(img_1);

% Add a circular object at 0.2, 0.5
% Calculate element membership in object
img_2 = img_1;
select_fcn = inline('(x-0.2).^2+(y-0.5).^2<0.1^2','x','y','z');
img_2.elem_data = 1 + elem_select(img_2.fwd_model, select_fcn);

disp(img_2.elem_data ...)


h2= subplot(222);
show_fem(img_2);
img_2.calc_colours.cb_shrink_move = [.3,.8,-0.02];
common_colourbar([h1,h2],img_2);
print_convert forward_solvers01a.png
