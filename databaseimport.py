import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import argparse
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 命令行参数解析
def parse_args():
    parser = argparse.ArgumentParser(description='用户数据聚类分析')
    parser.add_argument('--csv_file', default='D:\\DataAlysis\\淘宝用户行为.csv', help='CSV文件路径')
    parser.add_argument('--db_url', default='mysql+pymysql://root:123456@localhost:3306/taobao', help='数据库连接URL')
    parser.add_argument('--n_clusters', type=int, default=4, help='聚类簇数')
    parser.add_argument('--random_state', type=int, default=42, help='随机种子')
    return parser.parse_args()

def main():
    args = parse_args()
    
    try:
        # 读取CSV文件
        logging.info('开始读取CSV文件...')
        df = pd.read_csv(args.csv_file)
        logging.info(f'CSV文件读取成功，共 {len(df)} 条记录')
        
        # 将数据中的时间转化为datetime类型
        if 'invoice_date' in df.columns:
            df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%Y/%m/%d")
            logging.info('时间列处理完成')
        
        # 连接数据库
        logging.info('连接数据库...')
        engine = create_engine(args.db_url)
        
        # 将数据写入数据库
        df.to_sql(
            name="taobao_user_behavior",
            con=engine,
            if_exists='replace',
            index=False
        )
        logging.info('CSV数据已成功写入数据库 taobao_user_behavior 表')
        
        # 读取 user_rfm_result 表数据
        logging.info('从数据库读取 user_rfm_result 表数据...')
        df_rfm = pd.read_sql(-'SELECT * FROM user_rfm_result', con=engine)
        logging.info(f'user_rfm_result 表读取成功，共 {len(df_rfm)} 条记录')
        
        # 将数据保存为 CSV 文件
        df_rfm.to_csv('user_rfm_result.csv', index=False, encoding='utf-8-sig')
        logging.info('user_rfm_result 数据已保存为 user_rfm_result.csv 文件')
        
        # K-means 聚类分析
        logging.info(f'开始 K-means 聚类分析 (簇数: {args.n_clusters})...')
        
        # 准备特征数据（使用 recency, frequency, monetary 列）
        features = df_rfm[['recency', 'frequency', 'monetary']]
        
        # 数据标准化
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        logging.info('数据标准化完成')
        
        # 执行 K-means 聚类
        kmeans = KMeans(n_clusters=args.n_clusters, random_state=args.random_state)
        clusters = kmeans.fit_predict(scaled_features)
        logging.info('K-means 聚类完成')
        
        # 将聚类结果添加到 DataFrame
        df_rfm['cluster'] = clusters
        
        # 显示聚类结果
        logging.info('聚类结果统计：')
        cluster_counts = df_rfm['cluster'].value_counts()
        logging.info(f'{cluster_counts.to_dict()}')
        
        logging.info('各簇的特征统计：')
        cluster_stats = df_rfm.groupby('cluster')[['recency', 'frequency', 'monetary']].mean()
        logging.info(f'{cluster_stats.to_dict()}')
        
        # 读取 cluster_analysis_result 表数据
        logging.info('从数据库读取 cluster_analysis_result 表数据...')
        df_cluster = pd.read_sql('SELECT * FROM cluster_analysis_result', con=engine)
        
        logging.info(f'cluster_analysis_result 表读取成功，共 {len(df_cluster)} 条记录')
        logging.info(f'列名: {list(df_cluster.columns)}')
        
        # 根据性别比例和主要购买商品占比生成详细标签
        def generate_cluster_label(row):
            # 确定主要性别
            gender = '女性' if row['female_pct'] > row['male_pct'] else '男性'
            
            # 根据消费金额和活跃度确定用户价值
            if row['cluster'] == 0:
                value_type = '流失用户'
            elif row['cluster'] == 1:
                value_type = '中等价值用户'
            elif row['cluster'] == 2:
                value_type = '高价值用户'
            else:
                value_type = '低活跃用户'
            
            # 生成详细标签
            label = f"{gender}{value_type}({row['main_category']}消费占比{row['category_spend_pct']:.1f}%)"
            
            return label
        
        df_cluster['detailed_label'] = df_cluster.apply(generate_cluster_label, axis=1)
        
        # 显示各簇详细信息
        logging.info('各簇详细标签：')
        for idx, row in df_cluster.iterrows():
            logging.info(f"簇 {row['cluster']} ({row['detailed_label']}): 用户数量={row['total_users']}, "
                         f"性别比例=男性 {row['male_pct']:.1f}% / 女性 {row['female_pct']:.1f}%, "
                         f"主要购买类别={row['main_category']}, "
                         f"类别消费占比={row['category_spend_pct']:.1f}%")
        
        # 将详细标签映射到用户数据
        cluster_label_map = dict(zip(df_cluster['cluster'], df_cluster['detailed_label']))
        df_rfm['cluster_detailed_label'] = df_rfm['cluster'].map(cluster_label_map)
        
        # 保存包含详细标签的数据
        df_rfm.to_csv('user_rfm_clustered.csv', index=False, encoding='utf-8-sig')
        logging.info('聚类结果已保存为 user_rfm_clustered.csv 文件')
        
        # 将数据保存为 JSON 格式
        df_rfm.to_json('user_rfm_clustered.json', orient='records', force_ascii=False, indent=2)
        logging.info('聚类结果已保存为 user_rfm_clustered.json 文件')
        
        # 保存簇分析结果为 JSON 格式
        df_cluster.to_json('cluster_analysis.json', orient='records', force_ascii=False, indent=2)
        logging.info('簇分析结果已保存为 cluster_analysis.json 文件')
        
        # 将聚类结果写入数据库（直接使用内存中的数据，避免文件IO）
        df_rfm.to_sql(
            name="user_rfm_clustered",
            con=engine,
            if_exists='replace',
            index=False
        )
        logging.info('聚类结果已成功写入数据库 user_rfm_clustered 表')
        
    except Exception as e:
        logging.error(f'执行过程中发生错误: {str(e)}')
        raise
    finally:
        # 关闭数据库连接
        if 'engine' in locals():
            engine.dispose()
            logging.info('数据库连接已关闭')

if __name__ == '__main__':
    main()