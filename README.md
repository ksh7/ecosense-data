## EcoSense Data - Contributing Knowledge to Economy Discipline

EcoSense is an open-source economics data initiative that aims to improve practical knowledge of Economy subject.

### What it does?

It provides tailor-made datasets for various Economics topics accessible via APIs or downloadable as JSON files or Jupyter notebooks.

### How to use?

Visit: https://ecosense.joinabcenv.com to explore the portal and datasets.

### Accessing Datasets

To access a topic's datasets, applied questions, insights, etc. simply visit a topic's url. For example, for Lorenz Curve, visit: https://ecosense.joinabcenv.com/data/lorenz-curve

To access datasets via APIs for any topic use API url. For example: for Lorenz Curve, visit: https://ecosense.joinabcenv.com/api/lorenz-curve

List of all topics and datasets are provided in `datasets` directory.

### To Share Research Insights

Simply create an account on https://ecosense.joinabcenv.com/register and you can start sharing your economic research, insights with other users. You can make your insights `private` anytime you want to restrict access.

### Community vs Own Web App Instance To Share Research Insights

You can spin-up your own instance using `Dockerfile` available in `web-app` directory. Using your own instance, you won't need to depend on our community portal for sharing insights, research and even accessing datasets.

### Data Sources

Our datasets are generated using `AWS Data Exchange` portal's providers. We're using providers like Rearc DBNomics, PredictHQ, etc and plan to provide 1000+ customized datasets in future.

You can find list of data sources in `datasets` directory.

### Exporting to Econometric Softwares (WIP)
We are working on providing a way to directly export your datasets to Econometric Softwares like [E-VIEWS](https://www.eviews.com/home.html), [GRETL](https://gretl.sourceforge.net/) for better analysis and understanding.

### Contributing
We welcome economists, data scientist, and researchers to help us improve state of economy data by contributing to our initiative. Contributing guidelines and how-tos would be shared soon.

### Disclaimer
We do not claim to represent any of the providers at AWS Data Exchange. Amazon AWS & respective providers are the owner of data and they have right to restrict, deny any datasets.

In `version 0.1`, we are providing access to datasets using our AWS Data Exchange APIs for test purpose, but in upcoming `version 0.5` we plan to provide ability to add license, keys to access data individually by community users.
