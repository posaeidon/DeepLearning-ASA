"""
Runs n-body simulation of asteroids to see how close they approach Earth

*More information in the README.md

"""

__author__      = "John D. Hefele"
__email__       = "jdavidhefele@gmail.com"

from amuse.lab import *
from make_ss_1925 import *
import numpy as np
import os


def integrate_forward(pn_input,pn_output,dir_data,dt=0.02,total_t=500.):

    #Variables to alter
    max_asteroids=200
    dt= dt |units.yr
    total_t=total_t |units.yr

    #For setting printing options
    np.set_printoptions(linewidth=400, threshold=int(1e4), edgeitems=6)

    #Loads names of target asteroids
    asteroid_names=open(pn_input,'r')
    obj_name=asteroid_names.read().splitlines()
    obj_num=[]
    for i,row in enumerate(obj_name):
        #if i>0:
        split=row.strip('\n').split('\t')
        number=int(split[0])
        obj_num.append(number)
    num_asteroids=len(obj_num)
    if num_asteroids>max_asteroids:
        print('Running more than 200 asteroids at once will be slow!')

    print (obj_num)

    #Loads all asteroids coordinates
    fil_asteroid_coord=os.path.join(dir_data,'cart_asteroids.csv')
    print('Loading asteroid coordinates...')
    loaded_coords=np.genfromtxt(fil_asteroid_coord,delimiter=',')
    print('Done!')

    #Resets time and row number
    row_num=0
    t = 0 |units.yr

    #Initialize mercury
    converter = nbody_system.nbody_to_si(1.0 |units.MSun, 1.0 |units.AU)
    mer = Huayno(converter)
    mer.parameters.timestep = 0.05 |units.yr #Sets the initial timestep
    mer.initialize_code()

    #Creates the solar system and adds it to mercury
    ss=make_solar_system_1925(dir_data)
    mer.particles.add_particles(ss)

    #Find objects and sorts by epoch
    found_obj=[]
    for i,num in enumerate(obj_num):
        found_object=loaded_coords[np.where(loaded_coords[:,0] == num)]
        found_object.resize(found_object.size)
        found_obj.append(found_object)     
    object_matrix=np.array(found_obj)
    object_matrix=object_matrix[object_matrix[:,1].argsort()]

    #Integrates planets and objects forward
    num_added=0
    last_number=0
    int_names=[]
    x_values=[]; y_values=[]; z_values=[]
    full=False
    print('Adding asteroids to simulations...')
    while t < total_t:
        epoch=t.number+2424151.5
        mer.evolve_model(t)
        if t.number<95.:
            x=mer.particles.x.value_in(units.AU)
            y=mer.particles.y.value_in(units.AU)
            z=mer.particles.z.value_in(units.AU)
            sun_pos=[x[0],y[0],z[0]]
            if num_added==num_asteroids and full==False:
                print('All asteroids added!')
                full=True
            while num_added<num_asteroids:
                if object_matrix[row_num,1]>=epoch:
                    new_object = Particles(1)
                    new_object.position= object_matrix[row_num,2:5]+sun_pos |units.AU
                    new_object.velocity= object_matrix[row_num,5:8] |units.kms
                    new_object.mass = 1.0e-6 | units.g    # masses are negligible compared to Sun and planets, so we mostly ignore their
                                                        # effects. Their own dynamics of course do not depend on it, so we set it to a negligible number
                                                        # (1 micro gram)
                    mer.particles.add_particles(new_object)
                    int_names.append(object_matrix[row_num,0])
                    row_num+=1
                    num_added+=1
                else:
                    break
            t+=dt
        else:
            x_values.append(mer.particles.x.value_in(units.AU))
            y_values.append(mer.particles.y.value_in(units.AU))
            z_values.append(mer.particles.z.value_in(units.AU))
            t+=dt
        if int(t.number%50)==0 and int(t.number)!=last_number:
            print('%s of out of %s years integrated...'%(int(t.number),int(total_t.number)))
            
            last_number=int(t.number)
    print('Simulation complete!')

    #Closes down mercury
    mer.cleanup_code()
    mer.stop()

    x_matrix=np.array(x_values)
    y_matrix=np.array(y_values)
    z_matrix=np.array(z_values)
    num_steps,_=x_matrix.shape

    #Create a matrix of earth positions
    earth_positions=np.zeros((num_steps,3))       
    earth_positions[:,0]=x_matrix[:,3] 
    earth_positions[:,1]=y_matrix[:,3] 
    earth_positions[:,2]=z_matrix[:,3]

    #Creates matrices for each asteroid
    num_planets=int(10)
    asteroid_matrices=[]
    for i in range(num_asteroids):
        asteroid_positions=np.zeros((num_steps,3))
        asteroid_positions[:,0]=x_matrix[:,i+num_planets] 
        asteroid_positions[:,1]=y_matrix[:,i+num_planets] 
        asteroid_positions[:,2]=z_matrix[:,i+num_planets]
        asteroid_matrices.append(asteroid_positions)

    #Find minimum distance
    print('Appending objects to file %s'%(pn_output))
    output=open(pn_output,'a')
    for i in range(num_asteroids):
        min_distance=10000000
        for j in range(num_steps):
            distance=np.linalg.norm(earth_positions[j]-asteroid_matrices[i][j])
            if distance<min_distance:
                min_distance=distance
                time=2020.+j*dt.number
        output.write(str(int(int_names[i]))+" "+str(time)+" "+str(min_distance)+"\n")
    output.close()

    print('All computations successfully finished!')
    return earth_positions,asteroid_matrices

if __name__=='__main__':

    #pn_input should point to a file containing the integer names of the objects
    #pn_output should be the path and file name of the output (if it exist it will be appended) 
    #dt specifies the time step in years
    #total_t specifies the total integration time in years
    
    pn_input = 'non_hazardous_objects.txt'
    pn_output = 'output_nho.txt'
    dir_data='data'
    
    integrate_forward(pn_input,pn_output,dir_data)   














