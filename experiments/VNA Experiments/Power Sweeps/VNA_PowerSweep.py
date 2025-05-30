# %%
"""
    Test implementation of VNA driver
"""

from pathlib import Path
import sys, time, datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

current_dir = Path(".")
script_filename = Path(__file__).stem

sys.path.append(r"C:\Users\Lehnert Lab\GitHub") 

# from bcqt_hub.bcqt_hub.modules.DataAnalysis import DataAnalysis
import bcqthub.experiments.quick_helpers as qh

from bcqthub.bcqt_hub.drivers.instruments.VNA_Keysight import VNA_Keysight

# %% import VNA driver

### create dict to hold "default" configurations
VNA_Keysight_InstrConfig = {
    "instrument_name" : "VNA_Keysight",
    # "rm_backend" : "@py",
    "rm_backend" : None,
    "instr_addr" : 'TCPIP0::192.168.0.105::inst0::INSTR',
    "edelay" : 51.49,   #51.49ns for line1
    "averages" : 10,
    "sparam" : ['S21'],  
    
    # "segment_type" : "linear",                    
    # "segment_type" : "hybrid",
    "segment_type" : "homophasal",
}

### create instrument driver from "VNA_Keysight" class, which inherits BaseDriver
PNA_X = VNA_Keysight(VNA_Keysight_InstrConfig, debug=True)  

    

# %%

#all_freqs =  [   
            # MQC_BOE_SOLV1
#            4.3389418e9,
#            4.7333838e9,
#            5.1108957e9,
#            5.4838248e9,
#            5.8733538e9,
#            6.2299400e9,  # very low Q
#            6.6206182e9,  # very low Q
#            6.9972504e9   # very low Q
                      
#           ]

# all_freqs = [
#              # MQC_BOE_02
#              4.363937e9,
#              4.736494e9,
#              5.106847e9,
#              5.474224e9,
#              5.871315e9,
#              6.230610e9,  # very low Q
#              6.624036e9,  # very low Q
#             7.010525e9  # very low Q
#             ] 

# all_freqs = [
#             #  NW_DF_01
#             #  4.772140e9,
#             #  5.188173e9,
#             #  5.584948e9,
#             #  5.965468e9,
#             #  6.402026e9,
#             #  6.839330e9,  
#             #  7.258446e9,  
#             #  7.703534e9 
#             ] 

# all_freqs = [
#             #  NW_HF_01
#             #  4.399275e9,
#             #  4.807895e9,
#             #  5.178230e9,
#             #  5.542880e9,
#             #  5.895315e9,  # very low Q
#             #  6.298265e9,  # very low Q
#             #  6.701320e9,  # very low Q
#             #  7.103930e9  # very low Q
#             ] 

# all_freqs = [
#             #  Wide Sweep
#              4.5e9,
#              5.5e9, 
#              6.5e9, 
#              7.5e9 
#             ] 


ext_atten = 30

# ultra_high_powers = np.arange(10, 0, -1).round(2)
# high_powers = np.arange(-30,-46,-3).round(2) 
# med_powers = np.arange(-48, -64, -3).round(2) 
# low_powers = np.arange(-65, -73, -3).round(2) 
# ultra_low_powers = np.arange(-75, -85, -1).round(2) 
  
high_powers = np.arange(-30,-58,-3) 
med_powers = np.arange(-60, -73, -3)  
low_powers = np.arange(-73, -80, -2)  
ultra_low_powers = np.arange(-81, -86, -2)  

# high_powers = np.arange(-54,-58,-3) 
# med_powers = np.arange(-66, -73, -3)  
# low_powers = np.arange(-73, -80, -2)  
# ultra_low_powers = np.arange(-81, -86, -2)  

# For wide sweeping
# high_powers = np.arange(-30, -31, -3) 

# measure every power like normal
all_powers = [*high_powers, *med_powers, *low_powers, *ultra_low_powers]
# all_powers = [*high_powers, *med_powers, *low_powers]
# all_powers = [*med_powers, *low_powers]
# all_powers = [*ultra_low_powers]
# all_powers = [*high_powers]
# all_powers = [*med_powers]
print(all_powers)

# measure all even
# all_powers = [*high_powers[1::2], *med_powers[1::2], *low_powers[1::2], *ultra_low_powers[1::2]]

# measure all odds
# all_powers = [*high_powers[1::3], *med_powers[1::3], *low_powers[1::3], *ultra_low_powers[1::3]]

# measure one of each
# all_powers = [*high_powers[1:2], *med_powers[1:2], *low_powers[1:2], *ultra_low_powers[1:2]]

# atten_low_powers = [-40]


print(f"Measuring {len(all_freqs)} resonators and {len(all_powers)} powers for each. ({len(all_powers)*len(all_freqs)} measurements)")
time.sleep(1)

Measurement_Configs = {
    "f_span" : 1000e6, # the actual span is only half of f_span!
    "n_points" : 5001,
    "if_bandwidth" : 1000,
    "sparam" : ['S21'],  
    "Noffres" : 10,
}

# %% time estimation

num_res = len(all_freqs)

ETA_mins = sum([
    len(high_powers)*53 // 60,
    len(med_powers)*1093 // 60,
    len(low_powers)*2167 // 60,
    len(ultra_low_powers)*4366 // 60,
]) //10

now = datetime.datetime.now()
finishing_time = now + datetime.timedelta(minutes=ETA_mins*num_res)

display(f"{ETA_mins} minutes per resonator")
display(f"{num_res} total resonator(s) = {num_res*ETA_mins} minutes = {num_res*ETA_mins//60} hours total")

display(f" start time: {now.strftime("%m/%d, %I:%M:%S %p")}")
display(f"   end time: {finishing_time.strftime("%m/%d, %I:%M:%S %p")}")

# %%
def change_var_atten(power):
    current_path = Path(".")
    misc_path = Path("C:\Users\Lehnert Lab\GitHub\bcqt_hub\bcqt_hub\drivers\misc\MiniCircuits")
    instruments_path = Path("C:\Users\Lehnert Lab\GitHub\bcqt_hub\bcqt_hub\drivers\instruments")

    # easy access to all instrument drivers
    sys.path.append(str(current_path))
    sys.path.append(str(misc_path))
    sys.path.append(str(instruments_path))

    from MC_VarAttenuator import MC_VarAttenuator
    ip_addr_1 = "192.168.0.113"
        
    atten_1 = MC_VarAttenuator(ip_addr_1)
    atten_1.Set_Attenuation(power)
    

# %%
dstr = datetime.datetime.today().strftime("%m_%d_%H%M")

all_f_res = []
all_resonator_data = {}

tstart_all = time.time()
for idx, freq in enumerate(all_freqs):  # loop over all resonators
    freq_str = f"{freq/1e9:1.3f}".replace('.',"p")
    Measurement_Configs["f_center"] = freq
    resonator_name = f"Res{idx}_{freq_str}"
    
    res_power_sweep_dict = {}
    
    tstart_res = time.time()
    for power in all_powers:  # for each resonator, loop over all powers
        
        Measurement_Configs["power"] = power
        
        if power in ultra_high_powers:
            Measurement_Configs["averages"] = 100 
            print(f"{power} in ultra_high_powers - averages set to {Measurement_Configs["averages"]}")
        
        if power in high_powers:
            Measurement_Configs["averages"] = 2  # 53 seconds 
            print(f"{power} in high_powers - averages set to {Measurement_Configs["averages"]}")
            
        elif power in med_powers:
            Measurement_Configs["averages"] = 1000  # 1090 seconds
            print(f"{power} in med_powers - averages set to {Measurement_Configs["averages"]}")
        
        elif power in low_powers:
            Measurement_Configs["averages"] = 10000  # 2183 seconds 
            print(f"{power} in low_powers - averages set to {Measurement_Configs["averages"]}")
            
        elif power in ultra_low_powers:
            Measurement_Configs["averages"] = 20000  # 4366 seconds 
            print(f"{power} in ultra_low_powers - averages set to {Measurement_Configs["averages"]}")
            
            
        """ 
            use VNA to take & download data
        """
            
        ### update configs
        PNA_X.update_configs(**Measurement_Configs)
        
        ### compute segments for freq sweep
        Measurement_Configs["segments"] = PNA_X.compute_homophasal_segments() 
        
        ### send cmds to vna
        PNA_X.setup_s2p_measurement()
        
        ### run measurement
        PNA_X.run_measurement() 
        
        ### download and plot data
        s2p_df = PNA_X.return_data_s2p()
        axes = qh.plot_s2p_df(s2p_df, plot_complex=True, zero_lines=False)
        
        freqs = s2p_df["Frequency"][1:].to_numpy()
        magn = s2p_df["S21 magn_dB"][1:].to_numpy()
        
        f_res = round(freqs[magn.argmin()]/1e9,7)
        print(f"the data's lowest point is at {f_res=}")
        all_f_res.append(f_res)
        
        ### save data
        save_dir = r"./data/cooldown59/Line3_MQC_BOE_02"
        expt_category = rf"Line3_MQC_BOE_02_{dstr}"
        num_avgs = Measurement_Configs["averages"]
        meas_name = rf"{freq_str}GHz_{power:1.1f}dBm_{ext_atten}dBAtten_{num_avgs}avgs".replace(".","p")

        filename, filepath = qh.archive_data(PNA_X, s2p_df, meas_name=meas_name, save_dir=save_dir, expt_category=expt_category, all_axes=axes)

        
    tstop_res = time.time() - tstart_res
    display(f"Resonator {idx} (f_res={freq}) - {tstop_res:1.2f} seconds elapsed ({tstop_res/60:1.1f}) mins")
    
tstop_all = time.time() - tstart_all
display(f"Measurement finished - {tstop_all:1.2f} seconds elapsed ({tstop_all/60:1.1f}) mins")

# %%
""" 
    use scresonators to fit the data mid power-sweep
"""
        
        # Res_PowSweep_Analysis = DataAnalysis(None, dstr)
        # print(f"Fitting {filename}")
        
        # try:
        #     # output_params, conf_array, error, init, output_path
        #     params, conf_intervals, err, init1, fig = Res_PowSweep_Analysis.fit_single_res(data_df=s2p_df, save_dcm_plot=False, plot_title=filename, save_path=filepath)
        # except Exception as e:
        #     print(f"Failed to plot DCM fit for {power} dBm -> {filename}")
        #     continue
        
        # # 1/Q = 1/Qi + cos(phi)/|Qc|
        # # 1/Qi = 1/Q - cos(phi)/|Qc|
        # # Qi = 1/(1/Q - cos(phi)/|Qc|)
        
        # Q, Qc, f_center, phi = params
        # Q_err, Qi_err, Qc_err, Qc_Re_err, phi_err, f_center_err = conf_intervals
        
        # Qi = 1/(1/Q - np.cos(phi)/np.abs(Qc))
        
        # params = [Q, Qi, Qc, f_center, phi]
        
        # fit_results = {
        #     "power" : power,
        #     "Q" : Q,
        #     "Q_err" : Q_err,
        #     "Q_perc" : Q_err / Q,
            
        #     "Qi" : Qi,
        #     "Qi_err" : Qi_err,
        #     "Qi_perc" : Qi_err / Qi,
            
        #     "Qc" : Qc,
        #     "Qc_err" : Qc_err,
        #     "Qc_perc" : Qc_err / Qc,
            
        #     "f_center" : f_center,
        #     "f_center_err" : f_center_err,
        #     "phi" : phi,
        #     "phi_err" : phi_err,
        # }
        
        # res_power_sweep_dict[filename] = (s2p_df, fit_results, Measurement_Configs)
        # plt.show()

# %% use scresonators to plot data
        
    #     ### analyze data
        
    
    # all_resonator_data[resonator_name] = res_power_sweep_dict
    
    

    

# %% run analysis with scresonators


# init_params = [None]*4
# processed_data = { key : {"df": df, 
#                           "Measurement_Configs" : {**Measurement_Configs,  
#                                            "init_params" : init_params, 
#                                            "time_end" : time_end},  # add init_params and timestamp to config
#                           } 
#                   for key, (df, Measurement_Configs, time_end) in all_dfs.items() }

# Res_PowSweep_Analysis = DataAnalysis(processed_data, dstr)

    
# fit_results = {}
# for key, processed_data_dict in processed_data.items():
#     df, Measurement_Configs = processed_data_dict.values()
    
#     print(f"Fitting {key}")
    
#     power = Measurement_Configs["power"]
#     time_end = Measurement_Configs["time_end"]
    
#     save_dcm_plot = True if power <= -70 else False
    
#     if save_dcm_plot is not True:
#         continue
    
#     # output_params, conf_array, error, init, output_path
#     params, conf_intervals, err, init1, fig = Res_PowSweep_Analysis.fit_single_res(data_df=df, save_dcm_plot=False, plot_title=key, save_path=dcm_path)

#     # 1/Q = 1/Qi + cos(phi)/|Qc|
#     # 1/Qi = 1/Q - cos(phi)/|Qc|
#     # Qi = 1/(1/Q - cos(phi)/|Qc|)
    
#     Q, Qc, f_center, phi = params
#     Q_err, Qi_err, Qc_err, Qc_Re_err, phi_err, f_center_err = conf_intervals
    
#     Qi = 1/(1/Q - np.cos(phi)/np.abs(Qc))
    
#     params = [Q, Qi, Qc, f_center, phi]
    
#     parameters_dict = {
#         "power" : power,
#         "Q" : Q,
#         "Q_err" : Q_err,
#         "Qi" : Qi,
#         "Qi_err" : Qi_err,
#         "Qc" : Qc,
#         "Qc_err" : Qc_err,
#         "f_center" : f_center,
#         "f_center_err" : f_center_err,
#         "phi" : phi,
#         "phi_err" : phi_err,
#     }

#     perc_errs = {
#         "Q_perc" : Q_err / Q,
#         "Qi_perc" : Qi_err / Qi,
#         "Qc_perc" : Qc_err / Qc,
#     }
    
#     fit_results[key] = (df, Measurement_Configs, parameters_dict, perc_errs)
    
#     plt.show()
        
    
# %%

# all_param_dicts = {}
# for key, (df, Measurement_Configs, parameters_dict, perc_errs) in fit_results.items():
#     all_param_dicts[key] = parameters_dict
    
# df_fit_results = pd.DataFrame.from_dict(all_param_dicts, orient="index").reset_index()
# # df_fit_results.drop("phi_err", axis="columns", inplace=True)  


# n_pows = df_fit_results["power"].nunique()
# powers = df_fit_results["power"].unique()

# for param in ["Q", "Qi", "Qc"]:
    
#     fig, axes = plt.subplots(n_pows, 1, figsize=(10, 4*n_pows))
    
#     # handle case where we have single plot
#     if type(axes) != list:
#         fig.set_figheight(10)
#         axes = [axes]
        
#     for ax, power in zip(axes, powers):
        
#         threshold_percentage = 20
#         matching_powers = df_fit_results.loc[ df_fit_results["power"] == power]
        
#         # param = "Q"
#         dataset = matching_powers[param]
#         dataset_err = matching_powers[f"{param}_err"]
#         xvals = range(len(dataset))
        
#         avg, std = np.average(dataset), np.std(dataset)
        
#         failed_points = []
#         for x, pt, pt_err in zip(xvals, dataset, dataset_err):
#             perc_err = pt_err/pt * 100
            
#             if perc_err > threshold_percentage:
#                 info_str = f"idx{x}, {power=}: {param}={pt:1.1f} +/- {pt_err:1.1f}  ({perc_err=:1.1f}% > {threshold_percentage=}%)"
#                 failed_points.append((x, pt, pt_err, info_str))
#                 pt_color = 'r' 
#             else:
#                 pt_color = 'b'
                
#             ax.errorbar(x=x, y=pt, yerr=pt_err, color=pt_color, markersize=6, capsize=3)
        
#             ax.plot(x, pt, 'o', markersize=6, color=pt_color)
            
        
#         ax.axhline(avg, linestyle='--', linewidth=1, color='k', label=f"Average {param} = {avg:1.1e}")
        
#         ax.set_title(f"Power = {power} dBm")
#         # ax.set_yscale("log")
        
#         ax.set_xlabel("idx")
#         ax.set_ylabel(f"{param} Values")
#         ax.legend()


#         display(f"[{power = }] Failed Points: ")
#         for (x, pt, pt_err, info_str) in failed_points:
#             print(info_str)


#         fig.suptitle(f"Tracking {param} values over time, \n1 min/pt, \nthreshold = {threshold_percentage}% \n50 points per trace \n1 kHz IF_BW \n 1000 averages", size=18)
#         fig.tight_layout()
        
#     plt.show()

# %%
