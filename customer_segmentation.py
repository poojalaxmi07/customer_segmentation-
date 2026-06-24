'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Step 1: Load dataset
data = pd.read_csv(r"C:\customer-segmentation\data.csv")

# Step 2: Select features for clustering
X = data[['Age', 'Income', 'SpendingScore']]

# Step 3: Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Elbow Method to find optimal clusters
inertia = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    inertia.append(km.inertia_)

plt.plot(range(1, 11), inertia, marker='o')
plt.title("Elbow Method for Optimal k")
plt.xlabel("Number of clusters")
plt.ylabel("Inertia")
plt.savefig(r"C:\customer-segmentation\elbow_method.png")
plt.show()

# Step 5: Apply KMeans clustering (choose k=4 for example)
kmeans = KMeans(n_clusters=4, random_state=42)
data['Cluster'] = kmeans.fit_predict(X_scaled)

# Step 6: Visualize clusters
sns.scatterplot(x=data['Income'], y=data['SpendingScore'], hue=data['Cluster'], palette='Set2')
plt.title("Customer Segmentation")
plt.savefig(r"C:\customer-segmentation\cluster_plot.png")
plt.show()

# Step 7: Cluster summaries
cluster_summary = data.groupby('Cluster').mean()
print("Cluster Profiles:\n", cluster_summary)

# Step 8: Save results
data.to_csv(r"C:\customer-segmentation\segmented_customers.csv", index=False)
cluster_summary.to_csv(r"C:\customer-segmentation\cluster_summary.csv")

print("✅ Segmentation complete! Results saved to segmented_customers.csv and cluster_summary.csv")
print("✅ Plots saved as elbow_method.png and cluster_plot.png")'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Title
st.title("📊 Customer Segmentation Project")

# Upload dataset
uploaded_file = st.file_uploader("Upload your customer dataset (CSV)", type="csv")

if uploaded_file is not None:
    # Load dataset
    data = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Select features
    features = st.multiselect("Select features for clustering", data.columns, default=["Age", "Income", "SpendingScore"])
    if len(features) > 0:
        X = data[features]

        # Scale data
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Elbow Method
        inertia = []
        for k in range(1, 11):
            km = KMeans(n_clusters=k, random_state=42)
            km.fit(X_scaled)
            inertia.append(km.inertia_)

        fig, ax = plt.subplots()
        ax.plot(range(1, 11), inertia, marker='o')
        ax.set_title("Elbow Method for Optimal k")
        ax.set_xlabel("Number of clusters")
        ax.set_ylabel("Inertia")
        st.pyplot(fig)

        # Choose number of clusters
        k = st.slider("Select number of clusters (k)", 2, 10, 4)
        kmeans = KMeans(n_clusters=k, random_state=42)
        data['Cluster'] = kmeans.fit_predict(X_scaled)

        # Show cluster summary
        st.write("### Cluster Profiles")
        st.dataframe(data.groupby('Cluster').mean())

        # Scatter plot (if at least 2 features)
        if len(features) >= 2:
            fig, ax = plt.subplots()
            sns.scatterplot(x=data[features[0]], y=data[features[1]], hue=data['Cluster'], palette='Set2', ax=ax)
            ax.set_title("Customer Segmentation")
            st.pyplot(fig)

        # Download segmented data
        st.download_button("Download Segmented Data", data.to_csv(index=False).encode('utf-8'), "segmented_customers.csv", "text/csv")


