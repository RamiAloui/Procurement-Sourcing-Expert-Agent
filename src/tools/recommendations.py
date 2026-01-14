from typing import Dict, List
from src.tools.historical import get_latest_value
from src.tools.forecast import get_forecast, get_forecast_with_quantiles
from src.tools.comparative import compare_datasets


def recommend_forward_buy(
    dataset_name: str,
    months_ahead: int = 3,
    quantity: int = 1000,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Recommend whether to buy now or wait based on price forecasts.
    
    Analyzes current price vs forecast and provides buy/wait/monitor recommendation
    with quantified savings or costs.
    """
    # Get current price
    current = get_latest_value(dataset_name, data_path)
    
    # Get forecast
    forecast = get_forecast(dataset_name, months_ahead, data_path)
    
    # Calculate change
    price_change = forecast['forecast_value'] - current['value']
    pct_change = (price_change / current['value']) * 100
    
    # Determine recommendation based on price trend
    if pct_change > 2:
        recommendation = "buy_now"
        rationale = f"Price expected to rise {pct_change:.1f}%. Buy now to lock in lower price."
        savings = abs(price_change) * quantity
        action = "buying now"
    elif pct_change < -2:
        recommendation = "wait"
        rationale = f"Price expected to fall {abs(pct_change):.1f}%. Wait for lower prices."
        savings = abs(price_change) * quantity
        action = "waiting"
    else:
        recommendation = "monitor"
        rationale = "Price stable. No urgency to act. Monitor for changes."
        savings = 0
        action = "monitoring"
    
    # Check for high uncertainty
    if abs(pct_change) > 0.5 and abs(pct_change) <= 2:
        recommendation = "hedge"
        rationale = "Price movement uncertain. Consider buying 50-70% now, wait on rest."
        action = "hedging"
    
    return {
        'recommendation': recommendation,
        'current_price': round(current['value'], 2),
        'current_date': current['date'],
        'forecast_price': round(forecast['forecast_value'], 2),
        'forecast_date': forecast['date'],
        'price_change_pct': round(pct_change, 2),
        'price_change_abs': round(price_change, 2),
        'savings': round(savings, 2),
        'rationale': rationale,
        'action': action,
        'quantity': quantity
    }


def calculate_impact_analysis(
    dataset_name: str,
    months_ahead: int = 3,
    quantity: int = 1000,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Calculate quantified impact analysis with best/expected/worst scenarios.
    """
    current = get_latest_value(dataset_name, data_path)
    current_price = current['value']
    
    forecast_data = get_forecast_with_quantiles(dataset_name, months_ahead, data_path)
    
    q10 = forecast_data['quantile_0.1']
    q50 = forecast_data['quantile_0.5']
    q90 = forecast_data['quantile_0.9']
    
    price_direction = "rising" if q50 > current_price else "falling"
    
    if price_direction == "rising":
        best_case_price = q10
        expected_price = q50
        worst_case_price = q90
    else:
        best_case_price = q90
        expected_price = q50
        worst_case_price = q10
    
    def calculate_scenario(forecast_price, scenario_name):
        price_change = forecast_price - current_price
        pct_change = (price_change / current_price) * 100
        total_impact = price_change * quantity
        
        return {
            'scenario': scenario_name,
            'forecast_price': round(forecast_price, 2),
            'price_change_abs': round(price_change, 2),
            'price_change_pct': round(pct_change, 2),
            'total_impact': round(total_impact, 2),
            'impact_per_unit': round(price_change, 2)
        }
    
    best_case = calculate_scenario(best_case_price, "best_case")
    expected = calculate_scenario(expected_price, "expected")
    worst_case = calculate_scenario(worst_case_price, "worst_case")
    
    return {
        'dataset': dataset_name,
        'current_price': round(current_price, 2),
        'current_date': current['date'],
        'forecast_date': forecast_data['date'],
        'months_ahead': months_ahead,
        'quantity': quantity,
        'price_direction': price_direction,
        'best_case': best_case,
        'expected': expected,
        'worst_case': worst_case,
        'confidence_range': {
            'min': round(q10, 2),
            'median': round(q50, 2),
            'max': round(q90, 2)
        }
    }


def analyze_multi_commodity_scenario(
    dataset_names: List[str],
    months_ahead: int = 3,
    quantity: int = 1000,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Analyze complex scenarios involving multiple commodities.
    """
    recommendations = {}
    for dataset in dataset_names:
        rec = recommend_forward_buy(dataset, months_ahead, quantity, data_path)
        recommendations[dataset] = rec
    
    correlation_data = None
    if len(dataset_names) > 1:
        correlation_data = compare_datasets(dataset_names, data_path)
    
    prioritized = []
    
    for dataset, rec in recommendations.items():
        urgency = 0
        
        if rec['recommendation'] == 'buy_now':
            urgency = 3
        elif rec['recommendation'] == 'wait':
            urgency = 2
        else:
            urgency = 1
        
        price_change_magnitude = abs(rec['price_change_pct'])
        if price_change_magnitude > 5:
            urgency += 1
        
        prioritized.append({
            'dataset': dataset,
            'recommendation': rec['recommendation'],
            'urgency_score': urgency,
            'price_change_pct': rec['price_change_pct'],
            'savings': rec['savings'],
            'rationale': rec['rationale'],
            'current_price': rec['current_price'],
            'forecast_price': rec['forecast_price']
        })
    
    prioritized.sort(key=lambda x: x['urgency_score'], reverse=True)
    
    insights = []
    
    if correlation_data and 'correlation' in correlation_data:
        corr = correlation_data['correlation']
        if abs(corr) > 0.5:
            direction = "positive" if corr > 0 else "negative"
            insights.append(
                f"Commodities show {direction} correlation ({corr:.2f}). "
                f"Price movements tend to move {'together' if corr > 0 else 'opposite'}."
            )
    
    buy_count = sum(1 for p in prioritized if p['recommendation'] == 'buy_now')
    wait_count = sum(1 for p in prioritized if p['recommendation'] == 'wait')
    
    if buy_count > 0 and wait_count > 0:
        insights.append(
            f"Mixed signals: {buy_count} commodity(ies) rising, {wait_count} falling. "
            "Consider staggered procurement strategy."
        )
    
    return {
        'datasets_analyzed': dataset_names,
        'months_ahead': months_ahead,
        'individual_recommendations': recommendations,
        'prioritized_actions': prioritized,
        'correlation_data': correlation_data,
        'insights': insights,
        'total_potential_savings': sum(p['savings'] for p in prioritized)
    }


def recommend_production_sequencing(
    dataset_names: List[str],
    months_ahead: int = 3,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Recommend production sequencing based on commodity forecasts.
    """
    commodity_analysis = []
    
    for dataset in dataset_names:
        current = get_latest_value(dataset, data_path)
        forecast = get_forecast(dataset, months_ahead, data_path)
        
        price_change = forecast['forecast_value'] - current['value']
        pct_change = (price_change / current['value']) * 100
        
        if pct_change <= 0:
            favorability = "favorable"
            priority = 1
        elif pct_change <= 2:
            favorability = "moderately_favorable"
            priority = 2
        else:
            favorability = "unfavorable"
            priority = 3
        
        commodity_analysis.append({
            'dataset': dataset,
            'current_price': round(current['value'], 2),
            'forecast_price': round(forecast['forecast_value'], 2),
            'price_change_pct': round(pct_change, 2),
            'favorability': favorability,
            'priority': priority,
            'current_date': current['date'],
            'forecast_date': forecast['date']
        })
    
    commodity_analysis.sort(key=lambda x: x['priority'])
    
    sequence = []
    favorable_commodities = []
    unfavorable_commodities = []
    
    for i, commodity in enumerate(commodity_analysis, 1):
        if commodity['favorability'] == 'favorable':
            recommendation = f"Prioritize production using {commodity['dataset']} (prices falling {abs(commodity['price_change_pct']):.1f}%)"
            favorable_commodities.append(commodity['dataset'])
        elif commodity['favorability'] == 'moderately_favorable':
            recommendation = f"Schedule production using {commodity['dataset']} normally (prices stable)"
            favorable_commodities.append(commodity['dataset'])
        else:
            recommendation = f"Delay production using {commodity['dataset']} if possible (prices rising {commodity['price_change_pct']:.1f}%)"
            unfavorable_commodities.append(commodity['dataset'])
        
        sequence.append({
            'sequence_order': i,
            'dataset': commodity['dataset'],
            'recommendation': recommendation,
            'favorability': commodity['favorability'],
            'price_trend': commodity['price_change_pct']
        })
    
    total_favorable_change = sum(
        c['price_change_pct'] for c in commodity_analysis 
        if c['favorability'] in ['favorable', 'moderately_favorable']
    )
    total_unfavorable_change = sum(
        c['price_change_pct'] for c in commodity_analysis 
        if c['favorability'] == 'unfavorable'
    )
    
    insights = []
    
    if len(favorable_commodities) > 0:
        insights.append(
            f"Prioritize production using {', '.join(favorable_commodities)} "
            f"to take advantage of favorable price trends."
        )
    
    if len(unfavorable_commodities) > 0:
        insights.append(
            f"Consider delaying production using {', '.join(unfavorable_commodities)} "
            f"as prices are expected to rise."
        )
    
    if total_favorable_change < 0 and len(favorable_commodities) > 0:
        insights.append(
            f"Overall favorable conditions: average price decrease of {abs(total_favorable_change/len(favorable_commodities)):.1f}% "
            f"for prioritized commodities."
        )
    
    return {
        'datasets_analyzed': dataset_names,
        'months_ahead': months_ahead,
        'commodity_analysis': commodity_analysis,
        'recommended_sequence': sequence,
        'favorable_commodities': favorable_commodities,
        'unfavorable_commodities': unfavorable_commodities,
        'insights': insights,
        'cost_impact_summary': {
            'favorable_trend': round(total_favorable_change, 2),
            'unfavorable_trend': round(total_unfavorable_change, 2)
        }
    }
