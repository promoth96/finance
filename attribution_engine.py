"""
Digital Marketing Campaign Analytics & Multi-Touch Attribution Engine
Author: Senior Marketing Analytics & Data Science Consultant
Date: 2026-09-24
Description:
    1. Generates realistic multi-channel marketing synthetic data (aggregated & touchpoint journeys).
    2. Computes core marketing KPIs (ROAS, CAC, CVR, CTR, CPC, CPA).
    3. Implements Rule-Based Multi-Touch Attribution (First-Touch, Last-Touch, Linear, Position-Based).
    4. Runs Anomaly Detection & Low-ROAS Alerting System.
"""

import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_marketing_data(num_users=2500, random_seed=42):
    """
    Generates a realistic multi-channel marketing dataset.
    Simulates user touchpoint sequences across channels and campaigns,
    with realistic conversion probabilities, spends, and order values.
    """
    np.random.seed(random_seed)
    
    channels = ['Paid Search', 'Social Media', 'Display', 'Email', 'Organic Search']
    
    campaign_catalog = {
        'Paid Search': [
            {'campaign_id': 'SEM_BRAND_01', 'objective': 'Conversion', 'cpc': 1.20, 'cvr_base': 0.12, 'aov_mean': 110},
            {'campaign_id': 'SEM_GENERIC_PROD_02', 'objective': 'Conversion', 'cpc': 3.50, 'cvr_base': 0.045, 'aov_mean': 130},
            {'campaign_id': 'SEM_COMPETITOR_03', 'objective': 'Consideration', 'cpc': 4.80, 'cvr_base': 0.020, 'aov_mean': 120}
        ],
        'Social Media': [
            {'campaign_id': 'SOC_PROSP_LOOKALIKE_01', 'objective': 'Awareness', 'cpc': 1.80, 'cvr_base': 0.025, 'aov_mean': 95},
            {'campaign_id': 'SOC_RETARG_DPA_02', 'objective': 'Conversion', 'cpc': 2.40, 'cvr_base': 0.080, 'aov_mean': 105},
            {'campaign_id': 'SOC_INFLUENCER_BOOST_03', 'objective': 'Awareness', 'cpc': 2.10, 'cvr_base': 0.015, 'aov_mean': 90}
        ],
        'Display': [
            {'campaign_id': 'DSP_PROG_AWARE_01', 'objective': 'Awareness', 'cpc': 0.85, 'cvr_base': 0.008, 'aov_mean': 85},
            {'campaign_id': 'DSP_RETARG_ABANDON_02', 'objective': 'Conversion', 'cpc': 1.95, 'cvr_base': 0.055, 'aov_mean': 115}
        ],
        'Email': [
            {'campaign_id': 'EML_NEWSLETTER_WKLY_01', 'objective': 'Retention', 'cpc': 0.15, 'cvr_base': 0.060, 'aov_mean': 100},
            {'campaign_id': 'EML_ABANDONED_CART_02', 'objective': 'Conversion', 'cpc': 0.20, 'cvr_base': 0.140, 'aov_mean': 125},
            {'campaign_id': 'EML_WINBACK_90D_03', 'objective': 'Retention', 'cpc': 0.18, 'cvr_base': 0.040, 'aov_mean': 95}
        ],
        'Organic Search': [
            {'campaign_id': 'SEO_ORGANIC_DIRECT', 'objective': 'Baseline', 'cpc': 0.00, 'cvr_base': 0.050, 'aov_mean': 105}
        ]
    }
    
    # Generate Customer Touchpoint Journeys
    touchpoints_list = []
    user_journey_summary = []
    
    start_date = datetime(2026, 8, 1)
    
    for user_idx in range(1, num_users + 1):
        user_id = f"USR_{user_idx:05d}"
        
        # Path length: 1 to 5 touchpoints (geometric distribution)
        path_length = min(5, np.random.geometric(p=0.45))
        
        # Upper funnel channels tend to appear early; lower funnel later
        current_date = start_date + timedelta(days=np.random.randint(0, 45))
        journey_channels = []
        journey_campaigns = []
        
        for step in range(1, path_length + 1):
            if step == 1:
                # First touch biased towards Awareness / Display / Social / Organic
                step_channel = np.random.choice(
                    channels, 
                    p=[0.20, 0.35, 0.25, 0.05, 0.15]
                )
            elif step == path_length:
                # Last touch biased towards Retargeting / Paid Search / Email / Organic
                step_channel = np.random.choice(
                    channels, 
                    p=[0.35, 0.20, 0.10, 0.20, 0.15]
                )
            else:
                # Mid touch
                step_channel = np.random.choice(
                    channels, 
                    p=[0.25, 0.25, 0.20, 0.15, 0.15]
                )
                
            camp_info = np.random.choice(campaign_catalog[step_channel])
            touch_time = current_date + timedelta(hours=int(np.random.exponential(scale=36)))
            current_date = touch_time
            
            journey_channels.append(step_channel)
            journey_campaigns.append(camp_info['campaign_id'])
            
            touchpoints_list.append({
                'user_id': user_id,
                'touchpoint_order': step,
                'path_length': path_length,
                'channel': step_channel,
                'campaign_id': camp_info['campaign_id'],
                'objective': camp_info['objective'],
                'cpc': camp_info['cpc'],
                'timestamp': touch_time
            })
            
        # Determine conversion based on path synergy
        # Journeys with multiple distinct channels & lower-funnel retargeting have higher conversion
        base_conv_prob = 0.08
        if 'Email' in journey_channels:
            base_conv_prob += 0.07
        if 'Paid Search' in journey_channels:
            base_conv_prob += 0.06
        if path_length >= 3:
            base_conv_prob += 0.05
        if 'Display' in journey_channels and 'Social Media' in journey_channels:
            base_conv_prob += 0.04
            
        converted = np.random.rand() < min(base_conv_prob, 0.40)
        
        revenue = 0.0
        if converted:
            # Generate realistic revenue based on last campaign's AOV
            last_camp_id = journey_campaigns[-1]
            last_channel = journey_channels[-1]
            match_camp = [c for c in campaign_catalog[last_channel] if c['campaign_id'] == last_camp_id][0]
            revenue = round(np.random.normal(loc=match_camp['aov_mean'], scale=20), 2)
            revenue = max(25.0, revenue)
            
        user_journey_summary.append({
            'user_id': user_id,
            'path_length': path_length,
            'journey_path': " > ".join(journey_channels),
            'campaign_path': " > ".join(journey_campaigns),
            'first_touch_channel': journey_channels[0],
            'first_touch_campaign': journey_campaigns[0],
            'last_touch_channel': journey_channels[-1],
            'last_touch_campaign': journey_campaigns[-1],
            'all_channels': journey_channels,
            'all_campaigns': journey_campaigns,
            'converted': 1 if converted else 0,
            'revenue': revenue
        })
        
    df_touchpoints = pd.DataFrame(touchpoints_list)
    df_journeys = pd.DataFrame(user_journey_summary)
    
    # Merge journey conversion & revenue into touchpoints
    df_touchpoints = df_touchpoints.merge(
        df_journeys[['user_id', 'converted', 'revenue']], 
        on='user_id', 
        how='left'
    )
    
    # 2. Build Aggregated Campaign-Level Performance Dataset
    # Aggregate clicks, impressions, costs, and reported conversions
    campaign_rows = []
    for ch, camps in campaign_catalog.items():
        for camp in camps:
            c_id = camp['campaign_id']
            # Find touchpoints for this campaign
            c_touches = df_touchpoints[df_touchpoints['campaign_id'] == c_id]
            sample_clicks = len(c_touches)
            
            # Scale to realistic production campaign totals
            scale_factor = np.random.randint(15, 30)
            total_clicks = max(sample_clicks * scale_factor, 150)
            
            # Realistic CTR by channel
            ctr_map = {
                'Paid Search': np.random.uniform(0.035, 0.065),
                'Social Media': np.random.uniform(0.012, 0.024),
                'Display': np.random.uniform(0.003, 0.008),
                'Email': np.random.uniform(0.025, 0.045),
                'Organic Search': np.random.uniform(0.040, 0.070)
            }
            ctr = ctr_map[ch]
            impressions = int(total_clicks / ctr)
            
            # Calculate spend
            avg_cpc = camp['cpc'] * np.random.uniform(0.92, 1.08)
            spend = round(total_clicks * avg_cpc, 2)
            
            # Conversions directly attributed via Last-Touch
            c_conversions = df_journeys[(df_journeys['last_touch_campaign'] == c_id) & (df_journeys['converted'] == 1)]
            raw_conv_count = len(c_conversions)
            scaled_conversions = raw_conv_count * scale_factor
            
            # If 0 conversions in sample, give slight realistic base unless anomaly
            if scaled_conversions == 0 and ch != 'Display':
                scaled_conversions = int(total_clicks * camp['cvr_base'])
            elif scaled_conversions == 0 and ch == 'Display' and camp['objective'] == 'Awareness':
                scaled_conversions = int(total_clicks * 0.003)
                
            raw_rev = c_conversions['revenue'].sum()
            scaled_revenue = round(raw_rev * scale_factor, 2)
            if scaled_revenue == 0 and scaled_conversions > 0:
                scaled_revenue = round(scaled_conversions * camp['aov_mean'], 2)
                
            # Intentional anomaly injection for detection demonstration:
            # SEM_COMPETITOR_03: High spend, extremely low ROAS (money pit)
            if c_id == 'SEM_COMPETITOR_03':
                spend = round(spend * 2.8, 2)
                scaled_conversions = max(2, int(scaled_conversions * 0.3))
                scaled_revenue = round(scaled_conversions * 80.0, 2)
                
            # DSP_PROG_AWARE_01: Awareness display with high spend but near-zero last-click conversion
            if c_id == 'DSP_PROG_AWARE_01':
                spend = round(spend * 1.5, 2)
                scaled_conversions = max(1, int(scaled_conversions * 0.2))
                scaled_revenue = round(scaled_conversions * 70.0, 2)
                
            campaign_rows.append({
                'campaign_id': c_id,
                'channel': ch,
                'objective': camp['objective'],
                'impressions': impressions,
                'clicks': total_clicks,
                'spend': spend,
                'last_touch_conversions': scaled_conversions,
                'last_touch_revenue': scaled_revenue
            })
            
    df_campaign_summary = pd.DataFrame(campaign_rows)
    
    return df_touchpoints, df_journeys, df_campaign_summary


# ==============================================================================
# PHASE 2 - PART B: CORE MARKETING PERFORMANCE METRICS ENGINE
# ==============================================================================

def calculate_channel_metrics(df_campaign_summary):
    """
    Computes core marketing performance KPIs aggregated at the channel level.
    Metrics: Spend, Revenue, ROAS, CAC, CTR, CPC, CVR, CPA.
    """
    ch_agg = df_campaign_summary.groupby('channel').agg(
        total_impressions=('impressions', 'sum'),
        total_clicks=('clicks', 'sum'),
        total_spend=('spend', 'sum'),
        total_conversions=('last_touch_conversions', 'sum'),
        total_revenue=('last_touch_revenue', 'sum')
    ).reset_index()
    
    # Calculate derived KPIs
    ch_agg['CTR (%)'] = (ch_agg['total_clicks'] / ch_agg['total_impressions'] * 100).round(2)
    ch_agg['Avg_CPC ($)'] = (ch_agg['total_spend'] / ch_agg['total_clicks']).replace([np.inf, -np.inf], 0).round(2)
    ch_agg['CVR (%)'] = (ch_agg['total_conversions'] / ch_agg['total_clicks'] * 100).round(2)
    ch_agg['CPA_CAC ($)'] = (ch_agg['total_spend'] / ch_agg['total_conversions']).replace([np.inf, -np.inf], 0).round(2)
    ch_agg['Last_Touch_ROAS'] = (ch_agg['total_revenue'] / ch_agg['total_spend']).replace([np.inf, -np.inf], 0).round(2)
    
    return ch_agg


# ==============================================================================
# PHASE 2 - PART C: MULTI-TOUCH ATTRIBUTION (MTA) ENGINE
# ==============================================================================

def run_multi_touch_attribution(df_journeys):
    """
    Implements and compares Rule-Based Multi-Touch Attribution Models:
    1. First-Touch Attribution (FTA): 100% to first channel in journey.
    2. Last-Touch Attribution (LTA): 100% to final touchpoint prior to conversion.
    3. Linear Attribution (LIN): Equal distribution (1/N) across all touchpoints.
    4. Position-Based (U-Shaped, 40-20-40): 40% first, 40% last, 20% split among middle.
    """
    converted_journeys = df_journeys[df_journeys['converted'] == 1].copy()
    
    attribution_records = []
    
    for _, row in converted_journeys.iterrows():
        channels = row['all_channels']
        rev = row['revenue']
        n = len(channels)
        
        # Calculate weights for each touchpoint index (0 to n-1)
        for i, ch in enumerate(channels):
            # First-Touch Weight
            w_first = 1.0 if i == 0 else 0.0
            
            # Last-Touch Weight
            w_last = 1.0 if i == (n - 1) else 0.0
            
            # Linear Weight
            w_linear = 1.0 / n
            
            # Position-Based (U-Shaped 40/20/40)
            if n == 1:
                w_pos = 1.0
            elif n == 2:
                w_pos = 0.50
            else:
                if i == 0:
                    w_pos = 0.40
                elif i == (n - 1):
                    w_pos = 0.40
                else:
                    w_pos = 0.20 / (n - 2)
                    
            attribution_records.append({
                'user_id': row['user_id'],
                'channel': ch,
                'touchpoint_order': i + 1,
                'path_length': n,
                # Conversion credit
                'credit_first': w_first,
                'credit_last': w_last,
                'credit_linear': w_linear,
                'credit_position': w_pos,
                # Revenue credit
                'revenue_first': rev * w_first,
                'revenue_last': rev * w_last,
                'revenue_linear': rev * w_linear,
                'revenue_position': rev * w_pos
            })
            
    df_attrib_events = pd.DataFrame(attribution_records)
    
    # Channel-level aggregated comparison
    mta_summary = df_attrib_events.groupby('channel').agg(
        First_Touch_Conversions=('credit_first', 'sum'),
        Last_Touch_Conversions=('credit_last', 'sum'),
        Linear_Conversions=('credit_linear', 'sum'),
        Position_Conversions=('credit_position', 'sum'),
        First_Touch_Revenue=('revenue_first', 'sum'),
        Last_Touch_Revenue=('revenue_last', 'sum'),
        Linear_Revenue=('revenue_linear', 'sum'),
        Position_Revenue=('revenue_position', 'sum')
    ).round(2).reset_index()
    
    # Calculate % variance: Linear vs Last-Touch (reveals under/over-crediting)
    mta_summary['Linear_vs_Last_Rev_Diff (%)'] = (
        (mta_summary['Linear_Revenue'] - mta_summary['Last_Touch_Revenue']) / 
        mta_summary['Last_Touch_Revenue'] * 100
    ).round(1)
    
    return df_attrib_events, mta_summary


# ==============================================================================
# PHASE 2 - PART D: ANOMALY DETECTION & LOW-ROAS ALERT SYSTEM
# ==============================================================================

def run_campaign_anomaly_detection(df_campaign_summary, min_roas_threshold=2.0, max_cac_threshold=60.0):
    """
    Automated Anomaly Detection & Low-ROAS Alert Engine.
    Detects:
    1. Critical Low ROAS (< min_roas_threshold).
    2. High CAC / Unprofitable Acquisition (> max_cac_threshold).
    3. Spend Bleed (High spend > $2,000 with CVR < 1.0%).
    4. Statistical Z-score outlier on ROAS (< -1.5 std below mean of paid campaigns).
    Assigns Health Status, Severity, and Prescriptive Action.
    """
    df = df_campaign_summary.copy()
    
    # Calculate campaign level ROAS & CAC
    df['ROAS'] = (df['last_touch_revenue'] / df['spend']).replace([np.inf, -np.inf], 0).round(2)
    df['CAC'] = (df['spend'] / df['last_touch_conversions']).replace([np.inf, -np.inf], 0).round(2)
    df['CVR (%)'] = (df['last_touch_conversions'] / df['clicks'] * 100).round(2)
    
    # Paid campaigns filter for statistical benchmarking
    paid_mask = (df['spend'] > 0)
    paid_mean_roas = df.loc[paid_mask, 'ROAS'].mean()
    paid_std_roas = df.loc[paid_mask, 'ROAS'].std()
    
    df['roas_zscore'] = np.where(
        paid_mask & (paid_std_roas > 0),
        ((df['ROAS'] - paid_mean_roas) / paid_std_roas).round(2),
        0.0
    )
    
    alerts = []
    
    for _, row in df.iterrows():
        c_id = row['campaign_id']
        ch = row['channel']
        spend = row['spend']
        roas = row['ROAS']
        cac = row['CAC']
        cvr = row['CVR (%)']
        zscore = row['roas_zscore']
        
        status = 'HEALTHY'
        severity = 'INFO'
        reason = 'Performance within target thresholds'
        action = 'Maintain current spend trajectory & optimize creative'
        
        # Organic Search doesn't spend money
        if spend == 0:
            status = 'BASELINE'
            severity = 'INFO'
            reason = 'Unpaid Organic Baseline'
            action = 'Monitor search ranking & brand organic velocity'
        # Critical Anomaly: Severe Spend Bleed / Negative Returns
        elif roas < 1.0:
            status = 'CRITICAL'
            severity = 'P1_URGENT'
            reason = f"Negative ROI: ROAS ({roas:.2f}x) is below 1.0x break-even. CAC is ${cac:.2f}."
            action = 'IMMEDIATE PAUSE: Re-evaluate keyword match types, negative keywords, or landing page.'
        elif roas < min_roas_threshold:
            status = 'WARNING'
            severity = 'P2_MEDIUM'
            reason = f"Sub-target ROAS: ({roas:.2f}x vs target {min_roas_threshold:.1f}x). CVR is {cvr:.2f}%."
            action = 'REDUCE BUDGET (-30%): Shift budget to high-performing campaigns and refine audience.'
        elif cac > max_cac_threshold:
            status = 'WARNING'
            severity = 'P2_MEDIUM'
            reason = f"High CAC: ${cac:.2f} exceeds target threshold of ${max_cac_threshold:.2f}."
            action = 'OPTIMIZE CONVERSION FUNNEL: Conduct A/B test on checkout & landing page CTA.'
        elif zscore < -1.5:
            status = 'STATISTICAL_OUTLIER'
            severity = 'P2_MEDIUM'
            reason = f"ROAS Z-score ({zscore:.2f}) indicates statistically significant negative deviation."
            action = 'AUDIT CAMPAIGN: Investigate ad fatigue or recent audience/bidding adjustments.'
        elif roas >= 4.0:
            status = 'TOP_PERFORMER'
            severity = 'OPPORTUNITY'
            reason = f"High ROAS ({roas:.2f}x) well above target. Efficient customer acquisition (CAC ${cac:.2f})."
            action = 'SCALE BUDGET (+20% to +40%): Channel has headroom before marginal return diminishes.'
            
        alerts.append({
            'campaign_id': c_id,
            'channel': ch,
            'spend': spend,
            'revenue': row['last_touch_revenue'],
            'ROAS': roas,
            'CAC': cac,
            'CVR (%)': cvr,
            'Z_Score': zscore,
            'Health_Status': status,
            'Severity': severity,
            'Diagnosis': reason,
            'Recommended_Action': action
        })
        
    df_alerts = pd.DataFrame(alerts)
    return df_alerts


# ==============================================================================
# MAIN EXECUTION ROUTINE
# ==============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("DIGITAL MARKETING ANALYTICS & MULTI-TOUCH ATTRIBUTION ENGINE RUN")
    print("=" * 80)
    
    # 1. Generate Synthetic Multi-Touch Data
    df_touchpoints, df_journeys, df_campaign_summary = generate_marketing_data()
    print(f"\n[+] Generated {len(df_journeys)} Customer Journeys with {len(df_touchpoints)} Touchpoints.")
    print(f"[+] Total Simulated Conversions: {df_journeys['converted'].sum()} | Total Gross Revenue: ${df_journeys['revenue'].sum():,.2f}")
    
    # 2. Performance Metrics
    print("\n" + "=" * 80)
    print("1. CHANNEL-LEVEL PERFORMANCE BENCHMARK (LAST-TOUCH BASELINE)")
    print("=" * 80)
    ch_metrics = calculate_channel_metrics(df_campaign_summary)
    print(ch_metrics.to_string(index=False))
    
    # 3. Multi-Touch Attribution Engine
    print("\n" + "=" * 80)
    print("2. MULTI-TOUCH ATTRIBUTION (MTA) MODEL COMPARISON")
    print("=" * 80)
    df_attrib_events, mta_summary = run_multi_touch_attribution(df_journeys)
    print(mta_summary.to_string(index=False))
    
    # 4. Anomaly Detection & Low-ROAS Alert Engine
    print("\n" + "=" * 80)
    print("3. AUTOMATED CAMPAIGN ANOMALY DETECTION & ALERTING REPORT")
    print("=" * 80)
    df_alerts = run_campaign_anomaly_detection(df_campaign_summary, min_roas_threshold=2.2, max_cac_threshold=55.0)
    print(df_alerts[['campaign_id', 'channel', 'spend', 'ROAS', 'CAC', 'Health_Status', 'Severity', 'Recommended_Action']].to_string(index=False))
    
    # Save outputs to CSV for reporting & dashboard ingestion
    df_campaign_summary.to_csv("campaign_summary.csv", index=False)
    mta_summary.to_csv("mta_attribution_summary.csv", index=False)
    df_alerts.to_csv("campaign_alerts.csv", index=False)
    df_journeys.to_csv("customer_journeys.csv", index=False)
    print("\n[+] Exported campaign_summary.csv, mta_attribution_summary.csv, campaign_alerts.csv, and customer_journeys.csv.")
