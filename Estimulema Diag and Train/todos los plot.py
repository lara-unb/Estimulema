global arrayt2, rh, cr, cont_fig, fig, plot_show, sel_test
    global rh_acx, rh_acy, rh_acz, cr_acx, cr_acy, cr_acz

    print("Vamos plotar")

    file = 'acel_r.txt'
    data = np.loadtxt(file, delimiter=';')
    # print(data)

    # print(data[0])
    # print(data[0, 0])
    time_test = data[:, 0]

    # data of signal
    signal_pulse = data[:, 4]
    plt.figure(1)
    t = np.arange(0, len(signal_pulse))
    plt.plot(t, signal_pulse, 'g')
    print("Sinal")

    eje_x = data[:, 1]
    eje_y = data[:, 2]
    eje_z = data[:, 3]
    

    # Normalize the axis from digital to g(m/s^2)
    bits_dac = 65536  # 2 ^ 16
    eje_x = eje_x / bits_dac
    eje_y = eje_y / bits_dac
    eje_z = eje_z / bits_dac

    eje_x2 = eje_x**2
    eje_y2 = eje_y**2
    eje_z2 = eje_z**2

    xyz = eje_x2 + eje_y2 + eje_z2

    eje_xyz = np.sqrt(xyz)  # Out vector

    """
    # para filtrar y hacer el detector de pico
    in_sx = eje_x[:500]
    in_sy = eje_y[:500]
    in_sz = eje_z[:500]
    """
    in_sxyz = eje_xyz[:500]

    """
    med_x = np.mean(in_sx)
    print("valor medio: " + str(med_x))
    std_x = np.std(in_sx)
    print("La desviacion standard es: " + str(std_x))

    med_y = np.mean(in_sy)
    print("valor medio: " + str(med_y))
    std_y = np.std(in_sy)
    print("La desviacion standard es: " + str(std_y))

    med_z = np.mean(in_sz)
    print("valor medio: " + str(med_z))
    std_z = np.std(in_sz)
    print("La desviacion standard es: " + str(std_z))
    """

    med_xyz = np.mean(in_sxyz)
    print("valor medio: " + str(med_xyz))
    std_xyz = np.std(in_sxyz)
    print("La desviacion standard es: " + str(std_xyz))

    # Threshold calculation based on standard deviations
    num_std = 5

    thsdx = num_std * std_x
    lin_thsdx = np.ones((len(eje_x), 1)) * (med_x + thsdx)
    # print(lin_thsdx)

    thsdy = num_std * std_y
    lin_thsdy = np.ones((len(eje_y), 1)) * (med_y + thsdy)
    # print(lin_thsdy)

    thsdz = num_std * std_z
    lin_thsdz = np.ones((len(eje_z), 1)) * (med_z + thsdz)
    # print(lin_thsdz)
 
    thsdxyz = num_std * std_xyz
    lin_thsdxyz = np.ones((len(eje_xyz), 1)) * (med_xyz + thsdxyz)
    # print(lin_thsdxyz)


    plt.figure(1)
    t = np.arange(0, len(eje_x))
    plt.plot(t, lin_thsdx, 'g')
    plt.title = 'Acceleration for X axis'
    plt.xlabel = 'time (s)'
    plt.ylabel = 'g(m/s^2)'
    plt.plot(t, eje_x, 'b', linewidth=0.3)

    plt.figure(2)
    t = np.arange(0, len(eje_y))
    plt.plot(t, lin_thsdy, 'g')
    plt.title = 'Acceleration for Y axis'
    plt.xlabel = 'time (s)'
    plt.ylabel = 'g(m/s^2)'
    plt.plot(t, eje_y, 'b', linewidth=0.5)

    plt.figure(3)
    t = np.arange(0, len(eje_z))
    plt.plot(t, lin_thsdz, 'g')
    plt.title = 'Acceleration for Z axis'
    plt.xlabel = 'time (s)'
    plt.ylabel = 'g(m/s^2)'
    plt.plot(t, eje_z, 'b', linewidth=0.3)
    """

    plt.figure(4)
    t = np.arange(0, len(eje_xyz))
    plt.plot(t, lin_thsdxyz, 'g')
    plt.title = 'Acceleration magnitude resulting from the XYZ axis'
    plt.xlabel = 'time (s)'
    plt.ylabel = 'g(m/s^2)'
    plt.plot(t, eje_xyz, 'b', linewidth=0.3)

    cut_off = 30
    fs = 1000
    order = 10

    """
    acx_fil = butter_lowpass_filter(eje_x, cut_off, fs, order)
    plt.figure(1)
    plt.plot(t, acx_fil, 'r', linewidth=1)

    acy_fil = butter_lowpass_filter(eje_y, cut_off, fs, order)
    plt.figure(2)
    plt.plot(t, acy_fil, 'r', linewidth=1)

    acz_fil = butter_lowpass_filter(eje_z, cut_off, fs, order)
    plt.figure(3)
    plt.plot(t, acz_fil, 'r', linewidth=1)
    """

    acxyz_fil = butter_lowpass_filter(eje_xyz, cut_off, fs, order)
    plt.figure(4)
    plt.plot(t, acxyz_fil, 'r', linewidth=1)

    plt.show()

    print("Ends plot desde archivo para aceleracion")

    # Make a vector about execution time of the test
  
    t_ini = time_test[0] * 1E-6
    acel_N = len(time_test)
    t_end = time_test[acel_N - 1] * 1E-6
    t_total = t_end - t_ini
    print("Total time of test acel: " + str(t_total))
    acel_Ts = t_total / acel_N
    acel_fs = 1 / acel_Ts
    acel_t = np.arange(t_ini + acel_Ts, t_end , acel_Ts)

    file = 'stim_r.txt'
    data_s = np.loadtxt(file, delimiter=';')
    time_stim = data_s[:, 2]
    t_ini_s = time_stim[0] * 1E-6
    last_line = len(time_stim)
    t_end_s = time_stim[last_line - 1] * 1E-6

    stim_t = np.arange(t_ini_s + acel_Ts, t_end_s , acel_Ts)
    stim_N = len(stim_t)

    acel_stim_delay = stim_N - acel_N
    stim_t = stim_t[acel_stim_delay:stim_N]
    stim_N = len(stim_t)
    acel_stim_start_delay = stim_t[1] - acel_t[1]

    stim_r_i = data[:, 5]

    # build stim signal

    stim_r_pulse_counter = 1
    thisstim_r = 0
    thisvalue = 0

    for k in range(1, acel_N):
        if (signal_pulse[k] - thisstim_r) > 0.5:
            # new pulse found
            #thisvalue = np.mean(stim_r((6 * stim_r_pulse_counter) - 6 + 2:(6 * stim_r_pulse_counter) + 1, 2))
            thisstim_r = 1
            stim_r_pulse_counter = stim_r_pulse_counter + 1
            print("New pulse")
        elif (thisstim_r - signal_pulse[k]) > .5:
            thisstim_r = 0;
            print("Nada")

        stim_r_i[k] = stim_r_i[k] * thisvalue

    t_total_s = t_end_s - t_ini_s

    print("Total time of test stim: " + str(t_total_s))

    dif_acel_stim = np.abs(t_total - t_total_s)
    print("diferencia de tiempo: " + str(dif_acel_stim))
    """

    print("Fin sinal")




    # propor e enviar nuevos valores para el valor de terapia
    ##