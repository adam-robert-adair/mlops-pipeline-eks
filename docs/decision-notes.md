# Decision notes

- Use FastAPI as a supported serving fallback if KServe is not available in the target EKS cluster.
- Keep all compute CPU-only for predictable and low cost operation.
- Use IRSA with scoped S3 permissions instead of static AWS credentials.
