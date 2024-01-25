import signal

import streamlit as st
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# Lotka-Volterra equations
def lotka_volterra(y, t, alpha, beta, gamma, delta):
    # y[0] - prey ; y[1] - predator
    dxdt = alpha * y[0] - beta * y[0] * y[1]
    dydt = delta * y[0] * y[1] - gamma * y[1]
    return [dxdt, dydt]


# Plot population dynamics
def plot_population(t, solution, label_x='Time', label_y='Population', title='Population Dynamics'):
    fig, ax = plt.subplots()
    ax.plot(t, solution[:, 0], label='Prey (x)')
    ax.plot(t, solution[:, 1], label='Predator (y)')
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.legend()
    ax.set_title(title)
    return fig


# Phase diagram plot
def plot_phase_diagram(solution, label_x='Prey (x)', label_y='Predator (y)', title='Phase Diagram'):
    fig, ax = plt.subplots()
    ax.plot(solution[:, 0], solution[:, 1])
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.set_title(title)
    return fig


# Pages definitions
def show_overview():
    st.markdown('''
    ## Wstęp
    Historycznie pierwszym formalnym opisem oddziaływania dwóch populacji w ekosystemie jest model Lotki–Volterra. Model ten jest używany do analizy dynamiki populacji. Dotyczy on układu drapieżnik–ofiara, ilustruje, jak populacja drapieżników żywi się gatunkiem ofiary, jak wzrost jednej populacji wpływa na drugą.
    ''')
    st.image('./img/foxvshare.jpg')
    st.markdown('''
    Przykładowo można analizować dzięki równianiu Lotki–Volterra dynamiczne oddziaływania pomiędzy populacją lisów, a zajęcy.
    ### Równanie
    Równanie Lotka-Volterra ma postać:
    ''')
    st.latex(r'\frac{dx}{dt} = \alpha x - \beta xy')
    st.latex(r'\frac{dy}{dt} = \delta xy - \gamma y')
    st.markdown(r'''
    ##### Ofiara (Prey)
    - $ \frac{dx}{dt} $ - tępo wzrostu populacji ofiar czasie $ t $
    - $ x $ - ilość populacji ofiary (liczba ofiar)
    - $ \alpha $ - Współczynnik przyrostu liczby ofiar w wyniku braku drapieżników
    - $ \beta $ - współczynnik umieralności ofiar ze względu na liczbę drapieżników
     
    
    ##### Drapieżnik (Predator)
    - $ \frac{dy}{dt} $ - tępo wzrostu populacji drapieżników w czasie $ t $
    - $ y $ - ilość populacji drapieżników (liczba drapieżników)
    - $ \delta $ - współczynnik reprodukcji drapieżników
    - $ \gamma $ - współczynnik śmiertelności drapieżników w wyniku braku ofiar
    
    ### Analiza
    Wykres przedstawia dynamiczne zmiany w populacji ofiar (na przykład zająców) i drapieżników (na przykład lisów) w czasie, ilustrując interakcje między dwoma populacjami w ekosystemie. Na wykresie fazowym, można zobaczyć wizualizację relacji między tymi dwoma populacjami w przestrzeni fazowej. Analiza tych dwóch wykresów jednocześnie pozwala zrozumieć cykliczne wzorce, stabilność populacji i dynamikę ekosystemu.
    ''')
    st.image('./img/foxhare.gif')

def show_graphs():
    st.header("Graphs")
    st.markdown("Model representation using charts.")

    st.sidebar.divider()
    # Parameters in sidebar
    alpha, beta, gamma, delta = 0.1, 0.1, 0.1, 0.1
    initial_populations = [5, 10]
    # Chart stop
    stop = 100

    # Examples
    st.sidebar.header('Examples')
    if st.sidebar.button('Wolves vs Elk'):
        alpha, beta, gamma, delta = 0.1, 0.02, 0.05, 0.01
        initial_populations = [10, 10]
        stop = 200
    if st.sidebar.button('Foxes vs Hares'):
        alpha, beta, gamma, delta = 1.0, 0.2, 1.0, 0.1
        initial_populations = [5, 10]
        stop = 50

    st.sidebar.divider()
    # Parameters
    st.sidebar.header('Model Parameters')
    alpha = st.sidebar.slider('Prey birth rate (α)', min_value=0.01, max_value=2.0, value=alpha)
    beta = st.sidebar.slider('Prey death rate (β)', min_value=0.01, max_value=2.0, value=beta)
    gamma = st.sidebar.slider('Predator birth rate (γ)', min_value=0.01, max_value=2.0, value=gamma)
    delta = st.sidebar.slider('Predator death rate (δ)', min_value=0.01, max_value=2.0, value=delta)

    # Initial populations
    initial_populations = st.sidebar.slider('Initial Populations (x, y)', min_value=1, max_value=20, value=initial_populations)

    # Time points
    t = np.linspace(0, 15, 1000)
    t2 = np.linspace(0, stop, 1000)

    # Solve the differential equations
    solution = odeint(lotka_volterra, initial_populations, t, args=(alpha, beta, gamma, delta))
    solution2 = odeint(lotka_volterra, initial_populations, t2, args=(alpha, beta, gamma, delta))

    # Plotting
    # populations charts
    fig1 = plot_population(t, solution)
    fig2 = plot_population(t2, solution2, title=f'Population Dynamics x{stop}')

    # phase diagram
    fig3 = plot_phase_diagram(solution2)

    # Display the plots
    st.pyplot(fig1)
    col1, col2 = st.columns(2)
    col2.pyplot(fig2)
    col1.pyplot(fig3)


def show_bibliography():
    st.balloons()
    st.markdown('''
    ## Bibliography
    Thank you for taking the time to explore my website. I hope that your experience here is both informative and enjoyable.
    
    ### Links: 
    [1] J.Stewart - Single Variable Essential Calculus: Early Transcendentals, v. 6th, p. 608-614
    
    [2] https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations
    
    [3] https://pl.wikipedia.org/wiki/R%C3%B3wnanie_Lotki-Volterry
    ''')


# # -------------- # #
if __name__ == "__main__":
    # # Site elements

    # Site title
    st.title('Predator-Prey Model Lotka-Volterra')

    # Sidebar
    # Navigation buttons
    st.sidebar.header('Navigation menu')
    selected_option = st.sidebar.radio("", ["Overview", "Graphs", "Bibliography"])

    # Overview site
    if selected_option == "Overview":
        show_overview()
    # Graphs display site
    elif selected_option == "Graphs":
        show_graphs()
    # Bibliography site
    elif selected_option == "Bibliography":
        show_bibliography()

    # Author information
    st.sidebar.divider()
    st.sidebar.markdown(":eyes: **Author:** [Mateusz Sygnator](https://sygnator.com) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Sygnator-blue)](https://www.linkedin.com/in/Sygnator/) [![GitHub](https://img.shields.io/github/followers/Sygnator?style=social)](https://github.com/Sygnator)")
