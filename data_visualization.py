import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Utility Functions
def get_color_scale(color_scheme):
    """Retrieve the color scale based on user selection."""
    color_scales = {
        "Plotly3": px.colors.sequential.Plotly3,
        "Plasma": px.colors.sequential.Plasma,
        "Viridis": px.colors.sequential.Viridis,
        "Cividis": px.colors.sequential.Cividis,
        "Inferno": px.colors.sequential.Inferno,
        "Magma": px.colors.sequential.Magma
    }
    return color_scales.get(color_scheme, px.colors.sequential.Plotly3)

# Application Main
def main():
    """Main function to run the Streamlit app with improved UI and UX."""
    st.sidebar.title('Data Visualization Options')
    st.sidebar.text('Configure your visualization options here.')

    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if st.sidebar.checkbox('Show Data Preview'):
            st.write("Dataframe Preview:")
            st.write(df.head())

        chart_title, color_scheme = get_chart_customizations_sidebar()
        chart_type = st.sidebar.selectbox("Select the chart type",
                                          ["Line Chart", "Bar Chart", "Pie Chart", "Heatmap"])

        with st.spinner('Please wait... generating the chart'):
            x_col, y_col = get_axes(df, chart_type) if chart_type != 'Heatmap' else (None, None)
            fig = generate_chart(df, chart_type, x_col, y_col)
            if fig:
                apply_chart_customizations(fig, chart_title, color_scheme)
                st.plotly_chart(fig)
            else:
                st.warning("Please select appropriate data for the chart.")
    else:
        st.info("Please upload a CSV file to proceed.")

def display_data_preview(df):
    """Display a preview of the data if the user opts to."""
    if st.checkbox('Show Data Preview'):
        st.write("Dataframe Preview:")
        st.write(df.head())

def get_chart_customizations_sidebar():
    """Retrieve user input for chart customizations."""
    chart_title = st.sidebar.text_input("Chart Title", "My Chart")
    color_scheme = st.sidebar.selectbox("Choose a color scheme", ["Plotly3", "Plasma", "Viridis", "Cividis", "Inferno", "Magma"])
    return chart_title, color_scheme

def plot_chart(df, chart_type, chart_title, color_scheme):
    """Plot the chart based on user selections."""
    x_col, y_col = get_axes(df, chart_type)
    fig = generate_chart(df, chart_type, x_col, y_col)
    apply_chart_customizations(fig, chart_title, color_scheme)
    st.plotly_chart(fig)

def get_axes(df, chart_type):
    """Get the axes for the chart."""
    if chart_type != 'Heatmap':
        x_col = st.selectbox("Select x-axis", options=df.columns)
        y_col = st.selectbox("Select y-axis", options=df.columns)
    else:
        x_col, y_col = None, None
    return x_col, y_col

def generate_chart(df, chart_type, x_col, y_col):
    """Generate the specified chart type."""
    if chart_type == "Line Chart":
        fig = generate_line_chart(df, x_col, y_col)
    elif chart_type == "Bar Chart":
        fig = generate_bar_chart(df, x_col, y_col)
    elif chart_type == "Pie Chart":
        fig = generate_pie_chart(df, x_col, y_col)
    elif chart_type == "Heatmap":
        fig = generate_heatmap(df)
    return fig

def generate_line_chart(df, x_col, y_col):
    """Generate a line chart."""
    line_width = st.slider("Line Width", 1, 10, 2)
    fig = px.line(df, x=x_col, y=y_col, line_shape="linear")
    fig.update_traces(line=dict(width=line_width))
    return fig

def generate_bar_chart(df, x_col, y_col):
    """Generate a bar chart."""
    fig = px.bar(df, x=x_col, y=y_col, text=y_col)
    return fig

def generate_pie_chart(df, x_col, y_col):
    """Generate a pie chart."""
    if x_col and y_col:
        if df[x_col].isnull().any() or df[y_col].isnull().any():
            st.write("The selected columns for the pie chart contain NaN values.")
            return None
        else:
            hole = st.slider("Donut Hole Size", 0.0, 0.5, 0.1)
            fig = px.pie(df, names=x_col, values=y_col, hole=hole)
            return fig
    else:
        st.write("Please select appropriate columns for the pie chart.")
        return None

def generate_heatmap(df):
    """Generate a heatmap."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        st.write("No numeric columns available for heatmap.")
        return None
    else:
        fig = px.imshow(numeric_df.corr(), text_auto=True)
        return fig

def apply_chart_customizations(fig, chart_title, color_scheme):
    """Apply customizations to the chart."""
    if fig:
        color_scale = get_color_scale(color_scheme)
        fig.update_layout(title=chart_title, colorway=color_scale)

if __name__ == "__main__":
    main()
