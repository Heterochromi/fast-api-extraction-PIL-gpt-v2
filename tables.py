# import tabula

# # Read PDF file
# tables = tabula.read_pdf("chunking/Baclofen.pdf", pages="all")

# # Convert to CSV (maintains formatting better than DataFrame)
# for i, table in enumerate(tables):
#     table.to_csv(f"table_{i}.csv", index=False)

# import os
# print(os.getenv("model"))




# for dim in [768, 256, 48, 16, 8]:

#     sent2_score = cos_sim(query_embedding, model.encode(sentence_2)[:dim])[0][0].tolist()
#     sent3_score = cos_sim(query_embedding, model.encode(sentence_3)[:dim])[0][0].tolist()

#     scores.append({
#         "dim": dim,
#         "sent1_score": sent1_score,
#         "sent2_score": sent2_score,
#         "sent3_score": sent3_score
#     })

# scores_df = pd.DataFrame(scores)
# print(scores_df.to_markdown(index=False))
