import streamlit as st

st.set_page_config(
    page_title="Report Assistant_test",
    page_icon="🐥",
    layout="wide",
)

import insert_logo 
from with_report import condition_select, overview_writer, preprocessing_init_data, choose_trans_metric, export_info, bullet_output, ch_ranking_writer, detail_writer, keyword_writer, history_writer

insert_logo.add_logo("withbrother_logo.png")

#보고서 유형 저장
if 'condition_set' not in st.session_state:
    st.session_state.condition_set = None

#df 저장
if 'df_set' not in st.session_state:
    st.session_state.df_set = None

#기간 저장
if 'period_set' not in st.session_state:
    st.session_state.period_set = None

#지표 유형별 리스트 저장
if 'metric_set' not in st.session_state:
    st.session_state.metric_set = None

#전환 지표 유형별 리스트 저장
if 'trans_metric_set' not in st.session_state:
    st.session_state.trans_metric_set = None

#오버뷰 결과물
if 'overview_result' not in st.session_state:
    st.session_state.overview_result = None

#매체별 결과물
if 'ch_ranking_result' not in st.session_state:
    st.session_state.ch_ranking_result = None

#소재별 결과물
if 'brnch_ranking_result' not in st.session_state:
    st.session_state.brnch_ranking_result = None

#소재구분별 결과물
if 'brnch_detail_result' not in st.session_state:
    st.session_state.brnch_detail_result = None

#캠페인별 결과물
if 'cmp_ranking_result' not in st.session_state:
    st.session_state.cmp_ranking_result = {}

#광고그룹별 결과물
if 'grp_ranking_result' not in st.session_state:
    st.session_state.grp_ranking_result = {}

#소재명/키워드별 결과물
if 'kwrd_ranking_result' not in st.session_state:
    st.session_state.kwrd_ranking_result = {}

#캠페인별 결과물
if 'da_cmp_ranking_result' not in st.session_state:
    st.session_state.da_cmp_ranking_result = {}

#광고그룹별 결과물
if 'da_grp_ranking_result' not in st.session_state:
    st.session_state.da_grp_ranking_result = {}

#소재명/키워드별 결과물
if 'da_kwrd_ranking_result' not in st.session_state:
    st.session_state.da_kwrd_ranking_result = {}

#운영히스토리
if 'history_result' not in st.session_state:
    st.session_state.history_result = {}

org_sort_orders = {
    '노출수': False,  # 내림차순
    '클릭수': False,  # 내림차순
    'CTR': False,  # 내림차순'
    'CPC': True,  # 오름차순
    '총비용': False,  # 내림차순
    '전환수': False,  # 내림차순
    'CPA': True,  # 오름차순
    'GA_전환수': False,  # 내림차순
    'GA_CPA': True,  # 오름차순
}

# Streamlit app layout
st.title('보고서 작성 도우미')

# 데이터 입력기
with st.sidebar: #원하는 소스를 만드는 곳
    st.sidebar.header('이곳에 데이터를 업로드하세요.')
    
    media_file = st.file_uploader(
        "매체 데이터 업로드 (Excel or CSV)",
        type=['xls','xlsx', 'csv'],
        key="uploader1"
    )
    ga_file = st.file_uploader(
        "GA 데이터 업로드 (Excel or CSV)",
        type=['xls','xlsx', 'csv'],
        key="uploader2"
    )

    history_file = st.file_uploader(
        "운영 히스토리 데이터 업로드 (Excel or CSV)",
        type=["xls", "xlsx", "csv"],
        key="uploader3"
    )


# 보고서 유형 선택
if st.session_state.condition_set is None: #처음 선택한 경우
    st.session_state.condition_set = condition_select.create_form()
else: #설정 완료 버튼 이후, 출력
    st.session_state.condition_set = condition_select.display_form(st.session_state.condition_set)


# 최초 보고서 유형 제출 및 파일 업로드 완료
if st.session_state.condition_set and (st.session_state.df_set is None) and (st.session_state.period_set is None) and (st.session_state.metric_set is None):
    st.session_state.df_set, st.session_state.period_set, st.session_state.metric_set = preprocessing_init_data.filtering_data(media_file, ga_file, history_file, st.session_state.condition_set)
# 이미 업로드한 경우
elif st.session_state.condition_set and (st.session_state.df_set is not None) and (st.session_state.period_set is not None) and (st.session_state.metric_set is not None):
    preprocessing_init_data.notice_analysis_period(st.session_state.condition_set)
    
    with st.spinner("데이터 가져오는 중..."):
        pass
# 보고서 유형이나 파일이 제출되지 않은 상태
else:
    st.write("1. 사이드 바에 매체, GA, 운영 데이터 파일을 업로드하고, 보고서 유형을 선택해 설정 완료 버튼을 눌러주세요.")

# 전환 지표 설정 전
if st.session_state.condition_set and (st.session_state.trans_metric_set is None):
    st.session_state.trans_metric_set = choose_trans_metric.create_form(st.session_state.metric_set)
# 전환 지표 설정 후
elif st.session_state.condition_set and (st.session_state.trans_metric_set is not None):
    st.session_state.trans_metric_set = choose_trans_metric.display_form(st.session_state.metric_set, st.session_state.trans_metric_set)
# 보고서 유형 설정 전
else:   
    st.write("2. 파일 업로드와 설정 완료 버튼을 누르면, 전환 지표 설정 창이 생깁니다.")

# 보고서 생성 시작
if st.session_state.trans_metric_set:
    with st.spinner("보고서 초안 생성 중..."):
        grouping_period = export_info.get_group_kwr(st.session_state.condition_set["analysis_period"])
    
    data_col, history_col = st.columns([3,2])
    if st.session_state.condition_set["commerce_or_not"] == "비커머스":

        with data_col:
            overview, sa_perform, da_perform  = st.tabs(["오버뷰","SA 성과","DA 성과"])
            with overview:

                if st.session_state.overview_result is None:
                    st.subheader('오버뷰')
                    with st.spinner('데이터 분석 중...'):
                        rounded_overview_df = overview_writer.overview_df(st.session_state.df_set['used_media'], st.session_state.df_set['used_ga'], st.session_state.metric_set, st.session_state.trans_metric_set, grouping_period, st.session_state.condition_set, st.session_state.period_set)
                        overview_statement, overview_statement_summary = overview_writer.writer(rounded_overview_df, rounded_overview_df.columns.to_list())
                
                    st.session_state.overview_result = {'overview_df':rounded_overview_df,'overview_statement':overview_statement,'overview_statement_summary':overview_statement_summary}
                    
                    st.write(rounded_overview_df)
                    with st.expander("전체 지표 별 변화 문구"):
                        bullet_output.print_dic_bullet(overview_statement)
                    bullet_output.print_dic_bullet(overview_statement_summary)
                else:
                    st.subheader('오버뷰')
                    st.write(st.session_state.overview_result['overview_df'])
                    with st.expander("전체 지표 별 변화 문구"):
                        bullet_output.print_dic_bullet(st.session_state.overview_result['overview_statement'])
                    bullet_output.print_dic_bullet(st.session_state.overview_result['overview_statement_summary'])

                
                if st.session_state.ch_ranking_result is None:
                    ch_ranking_df = ch_ranking_writer.ch_ranking_df(
                        st.session_state.df_set['used_media'],
                        st.session_state.df_set['used_ga'],
                        '매체',
                        st.session_state.metric_set,
                        st.session_state.trans_metric_set,
                        grouping_period,
                        st.session_state.condition_set,
                    )
                    

                    now_period_result, sort_order = ch_ranking_writer.display_period_data(
                        st.session_state.period_set["now"],
                        ch_ranking_df,
                        st.session_state.overview_result['overview_df'],
                        '매체',
                        grouping_period,
                        None
                    )


                    st.session_state.ch_ranking_result = {"now_result_df":now_period_result}

                    pre_period_result, _ = ch_ranking_writer.display_period_data(
                        st.session_state.period_set["pre"],
                        ch_ranking_df,
                        st.session_state.overview_result['overview_df'],
                        '매체',
                        grouping_period,
                        sort_order
                    )
                    

                    st.session_state.ch_ranking_result["pre_result_df"] = pre_period_result

                    st.session_state.ch_ranking_result["sort_order"] = sort_order
                    channels = [x for x in now_period_result['매체'].unique() if x != '합계']

                    ch_overview_df_dic = {}
                    ch_overview_st_dic = {}
                    ch_overview_st_dic_summary = {}
                    with st.spinner('데이터 분석 중...'):
                        for channel in channels:
                            if str(channel) == '정보없음':
                                continue
                            rounded_overview_ch_df = ch_ranking_writer.ch_df(
                                ch_ranking_df, '매체', channel, 
                                grouping_period,
                                st.session_state.period_set,
                                st.session_state.condition_set,
                            )
                            overview_ch_statement, overview_ch_statement_summary = overview_writer.writer(rounded_overview_ch_df, rounded_overview_ch_df.columns.to_list())
                            
                            ch_overview_df_dic[channel] = rounded_overview_ch_df
                            ch_overview_st_dic[channel] = overview_ch_statement
                            ch_overview_st_dic_summary[channel] = overview_ch_statement_summary

                    st.session_state.ch_ranking_result["ch_overview_df_dic"] = ch_overview_df_dic
                    st.session_state.ch_ranking_result["ch_overview_st_dic"] = ch_overview_st_dic
                    st.session_state.ch_ranking_result["ch_overview_st_dic_summary"] = ch_overview_st_dic_summary
                else:
                    pass
                
                brnch_dsply = 1

                if st.session_state.df_set['used_media']['소재구분'].isnull().all():
                    brnch_dsply = 0
                    #st.write('매체 데이터에서 소재구분 데이터가 없는 기간입니다.')
                else:
                    if st.session_state.brnch_ranking_result is None:
                        brnch_ranking_df = ch_ranking_writer.ch_ranking_df(
                            st.session_state.df_set['used_media'],
                            st.session_state.df_set['used_ga'],
                            '소재구분',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        now_period_result, sort_order = ch_ranking_writer.display_period_data(
                                st.session_state.period_set["now"],
                                brnch_ranking_df,
                                st.session_state.overview_result['overview_df'],
                                '소재구분',
                                grouping_period,
                                None
                            )

                        st.session_state.brnch_ranking_result = {"now_result_df":now_period_result}
                        

                        pre_period_result, _ = ch_ranking_writer.display_period_data(
                                st.session_state.period_set["pre"],
                                brnch_ranking_df,
                                st.session_state.overview_result['overview_df'],
                                '소재구분',
                                grouping_period,
                                sort_order
                            )

                        st.session_state.brnch_ranking_result["pre_result_df"] = pre_period_result

                        st.session_state.brnch_ranking_result["sort_order"] = sort_order
                        brnchs = [x for x in now_period_result['소재구분'].unique() if x != '합계']

                        brnch_overview_df_dic = {}
                        brnch_overview_st_dic = {}
                        brnch_overview_st_dic_summary = {}
                        with st.spinner('데이터 분석 중...'):
                            for brnch in brnchs:
                                if str(brnch) == '정보없음':
                                    continue
                                rounded_overview_brnch_df = ch_ranking_writer.ch_df(
                                    brnch_ranking_df, '소재구분', brnch, 
                                    grouping_period,
                                    st.session_state.period_set,
                                    st.session_state.condition_set,
                                )
                                overview_brnch_statement, overview_brnch_statement_summary = overview_writer.writer(rounded_overview_brnch_df, rounded_overview_brnch_df.columns.to_list())
                                
                                brnch_overview_df_dic[brnch] = rounded_overview_brnch_df
                                brnch_overview_st_dic[brnch] = overview_brnch_statement
                                brnch_overview_st_dic_summary[brnch] = overview_brnch_statement_summary


                        st.session_state.brnch_ranking_result["brnch_overview_df_dic"] = brnch_overview_df_dic
                        st.session_state.brnch_ranking_result["brnch_overview_st_dic"] = brnch_overview_st_dic
                        st.session_state.brnch_ranking_result["brnch_overview_st_dic_summary"] = brnch_overview_st_dic_summary

            with sa_perform:
                selected_ad_type = "SA"
                st.session_state.SA_result = {"ad_type":selected_ad_type}

                filtered_type_df = st.session_state.df_set['used_media'][st.session_state.df_set['used_media']["광고유형"] == selected_ad_type]
                filtered_ga_type_df = st.session_state.df_set['used_ga'][st.session_state.df_set['used_ga']["광고유형"] == selected_ad_type]

                st.write("분석하고자 하는 매체를 선택해주세요.")
                selected_channel = st.selectbox(
                    "매체 선택",
                    filtered_type_df["매체"].dropna().unique()
                )
                
                st.session_state.SA_result["channel"] = selected_channel
                st.session_state.cmp_ranking_result["channel"] = selected_channel

                overview_sa, cmp_sa, grp_sa, kwrd_sa  = st.tabs(["전체 성과 분석","캠페인 분석","그룹 분석", "성과 상위 키워드 분석"])
                with overview_sa:
                    st.subheader(selected_channel)
                    st.write(st.session_state.ch_ranking_result["ch_overview_df_dic"][selected_channel])
                    with st.expander("전체 지표 별 변화 문구"):
                        bullet_output.print_dic_bullet(st.session_state.ch_ranking_result["ch_overview_st_dic"][selected_channel])
                    bullet_output.print_dic_bullet(st.session_state.ch_ranking_result["ch_overview_st_dic_summary"][selected_channel])

                with cmp_sa:
                    sort_orders_cmp = org_sort_orders
                    metrics = st.session_state.overview_result['overview_df'].columns.tolist()

                    for metric in metrics:
                        if metric not in org_sort_orders.keys():
                            sort_orders_cmp[metric] = False
                        else:
                            pass
                    
                    submit_button_cmp, sort_columns_cmp = detail_writer.choose_metric(metrics,2)

                    st.session_state.cmp_ranking_result["submit_button"] = submit_button_cmp
                    st.session_state.cmp_ranking_result["metric_sort_order"] = sort_orders_cmp
                    st.session_state.cmp_ranking_result["selected_metrics"] = sort_columns_cmp

                    filtered_cmp_df = filtered_type_df[filtered_type_df["매체"] == selected_channel]
                    filtered_ga_cmp_df = filtered_ga_type_df[filtered_ga_type_df["매체"] == selected_channel]

                    st.session_state.cmp_ranking_result["cmp_df"] = filtered_cmp_df
                    st.session_state.cmp_ranking_result["ga_cmp_df"] = filtered_ga_cmp_df

                    if submit_button_cmp:

                        detail_cmp_df = ch_ranking_writer.ch_ranking_df(
                            filtered_cmp_df,
                            filtered_ga_cmp_df,
                            '캠페인',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )
                        
                        filtered_detail_cmp_df = detail_cmp_df[detail_cmp_df[grouping_period] == st.session_state.period_set["now"]]

                        sorted_cmp_df, top_cmp_num, cmp_statements = detail_writer.display_top(
                            sort_columns_cmp,
                            sort_orders_cmp,
                            filtered_detail_cmp_df, 
                            st.session_state.overview_result['overview_df'],
                        )

                        st.session_state.cmp_ranking_result['top_cmp_detail_df'] = sorted_cmp_df
                        st.session_state.cmp_ranking_result['top_num_cmp_detail'] = top_cmp_num
                        st.session_state.cmp_ranking_result['cmp_detail_statment'] = cmp_statements

                        st.write('정렬된 상위 ' + str(top_cmp_num) + '개 캠페인')
                        st.write(sorted_cmp_df)

                        for statement in cmp_statements:
                            st.write(statement)

                        try:
                            description_cmp_detail = detail_writer.writer(top_cmp_num, sorted_cmp_df, sort_columns_cmp)

                            st.session_state.cmp_ranking_result['description_cmp_detail'] = description_cmp_detail

                            #st.write(description_cmp_detail)
                            bullet_output.display_analysis(description_cmp_detail,sorted_cmp_df.columns.to_list())
                        except:
                            st.session_state.cmp_ranking_result['description_cmp_detail'] = "데이터 정합성을 확인해주세요."
                            st.write("데이터 정합성을 확인해주세요.")
                    else:
                        st.write('정렬 기준 지표를 선택한 후, 정렬 적용 버튼을 눌러주세요.')
                        if 'description_cmp_detail' in st.session_state.cmp_ranking_result.keys():
                            st.write('정렬된 상위 ' + str(st.session_state.cmp_ranking_result['top_num_cmp_detail']) + '개 매체')
                            st.write(st.session_state.cmp_ranking_result['top_cmp_detail_df'])

                            for statement in st.session_state.cmp_ranking_result['cmp_detail_statment']:
                                st.write(statement)
                            #st.write(st.session_state.cmp_ranking_result['description_cmp_detail'])
                            try:
                                bullet_output.display_analysis(st.session_state.cmp_ranking_result['description_cmp_detail'],st.session_state.cmp_ranking_result['top_cmp_detail_df'].columns.to_list())
                            except:
                                st.write("데이터 정합성을 확인해주세요.")
                with grp_sa:
                    st.header("그룹 분석")
                    st.write("분석하고자 하는 캠페인을 선택해주세요.")
                    if 'description_cmp_detail' in st.session_state.cmp_ranking_result.keys():
                        st.write("아래는 " + st.session_state.cmp_ranking_result["channel"] + "의 캠페인 목록입니다.")
                        
                        selected_campaign = st.selectbox(
                            "캠페인 선택",
                            st.session_state.cmp_ranking_result["cmp_df"]["캠페인"].dropna().unique(),
                        )

                        st.session_state.grp_ranking_result = {"campaign" : selected_campaign}

                        filtered_grp_df = st.session_state.df_set["used_media"][(st.session_state.df_set["used_media"]["매체"] == st.session_state.cmp_ranking_result["channel"]) & (st.session_state.df_set["used_media"]["캠페인"] == selected_campaign)]
                        filtered_ga_grp_df = st.session_state.df_set["used_ga"][(st.session_state.df_set["used_ga"]["매체"] == st.session_state.cmp_ranking_result["channel"]) & (st.session_state.df_set["used_ga"]["캠페인"] == selected_campaign)]

                        st.session_state.grp_ranking_result["grp_df"] = filtered_grp_df
                        st.session_state.grp_ranking_result["ga_grp_df"] = filtered_ga_grp_df

                        detail_grp_df = ch_ranking_writer.ch_ranking_df(
                            filtered_grp_df,
                            filtered_ga_grp_df,
                            '광고그룹',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        filtered_detail_grp_df = detail_grp_df[detail_grp_df[grouping_period] == st.session_state.period_set["now"]]

                        if len(filtered_detail_grp_df) == 0:
                            st.write("이번 기간에는 운영되지 않은 캠페인입니다.")
                        else:
                            sorted_grp_df, top_grp_num, grp_statements = detail_writer.display_top(
                                st.session_state.cmp_ranking_result["selected_metrics"],
                                st.session_state.cmp_ranking_result["metric_sort_order"],
                                filtered_detail_grp_df, 
                                st.session_state.overview_result['overview_df'],
                            )

                            st.session_state.grp_ranking_result['top_grp_detail_df'] = sorted_grp_df
                            st.session_state.grp_ranking_result['top_num_grp_detail'] = top_grp_num
                            st.session_state.grp_ranking_result['grp_detail_statment'] = grp_statements

                            st.write('정렬된 상위 ' + str(top_grp_num) + '개 광고그룹')
                            st.write(sorted_grp_df)

                            for statement in grp_statements:
                                st.write(statement)

                            try:
                                description_grp_detail = detail_writer.writer(top_grp_num, sorted_grp_df, st.session_state.cmp_ranking_result["selected_metrics"])

                                st.session_state.grp_ranking_result['description_grp_detail'] = description_grp_detail

                                #st.write(description_grp_detail)
                                bullet_output.display_analysis(description_grp_detail, sorted_grp_df.columns.to_list())
                            except:
                                st.write("데이터 정합성을 확인해주세요.")
                    else:
                        st.write("캠페인 분석 탭을 먼저 실행해주세요.")
                with kwrd_sa:
                    st.header("키워드별 성과 분석")
                    st.write("성과 상위 키워드를 분석합니다.")
                    if "campaign" in st.session_state.grp_ranking_result.keys():
                        st.write("선택된 매체 : " + st.session_state.cmp_ranking_result["channel"])
                        st.write("선택된 캠페인 : " + st.session_state.grp_ranking_result["campaign"])
                        st.write("선택된 지표 : " + ",".join(st.session_state.cmp_ranking_result["selected_metrics"]))

                        detail_kwrd_df = ch_ranking_writer.ch_ranking_df(
                            st.session_state.grp_ranking_result["grp_df"],
                            st.session_state.grp_ranking_result["ga_grp_df"],
                            '소재명/키워드',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        filtered_detail_kwrd_df = detail_kwrd_df[detail_kwrd_df[grouping_period] == st.session_state.period_set["now"]]
                        
                        if len(filtered_detail_kwrd_df) == 0:
                            st.write("이번 기간에는 운영되지 않은 캠페인입니다.")
                        else:
                            keyword_ranking_df = keyword_writer.kwrd_ranking_df(
                                st.session_state.df_set['used_media'],
                                st.session_state.df_set['used_ga'],
                                st.session_state.metric_set,
                                st.session_state.trans_metric_set,
                                grouping_period,
                                st.session_state.condition_set,
                            )

                            kwrd_statements = keyword_writer.writer(
                                filtered_detail_kwrd_df,
                                keyword_ranking_df, 
                                st.session_state.cmp_ranking_result["selected_metrics"],
                                st.session_state.cmp_ranking_result["metric_sort_order"],
                            )

                    else:
                        st.write("캠페인 분석 탭을 먼저 실행해주세요.")
            with da_perform:
                selected_ad_type = "DA"
                st.session_state.DA_result = {"ad_type":selected_ad_type}

                filtered_type_df = st.session_state.df_set['used_media'][st.session_state.df_set['used_media']["광고유형"] == selected_ad_type]
                filtered_ga_type_df = st.session_state.df_set['used_ga'][st.session_state.df_set['used_ga']["광고유형"] == selected_ad_type]

                st.write("분석하고자 하는 매체를 선택해주세요.")
                selected_channel = st.selectbox(
                    "매체 선택",
                    filtered_type_df["매체"].dropna().unique()
                )
                
                st.session_state.da_cmp_ranking_result["channel"] = selected_channel
                overview_da, cmp_da, grp_da, brnch_da, brnch_dtl_da, kwrd_da  = st.tabs(["전체 성과 분석","캠페인 분석","그룹 분석", "소재구분 분석", "소재종류 분석", "성과 상위 소재 분석"])
                with overview_da:
                    st.subheader(selected_channel)
                    st.write(st.session_state.ch_ranking_result["ch_overview_df_dic"][selected_channel])
                    with st.expander("전체 지표 별 변화 문구"):
                        bullet_output.print_dic_bullet(st.session_state.ch_ranking_result["ch_overview_st_dic"][selected_channel])
                    bullet_output.print_dic_bullet(st.session_state.ch_ranking_result["ch_overview_st_dic_summary"][selected_channel])
                with cmp_da:
                    sort_orders_cmp = org_sort_orders
                    metrics = st.session_state.overview_result['overview_df'].columns.tolist()

                    for metric in metrics:
                        if metric not in org_sort_orders.keys():
                            sort_orders_cmp[metric] = False
                        else:
                            pass
                    
                    submit_button_cmp, sort_columns_cmp = detail_writer.choose_metric(metrics,3)

                    st.session_state.da_cmp_ranking_result["submit_button"] = submit_button_cmp
                    st.session_state.da_cmp_ranking_result["metric_sort_order"] = sort_orders_cmp
                    st.session_state.da_cmp_ranking_result["selected_metrics"] = sort_columns_cmp

                    filtered_cmp_df = filtered_type_df[filtered_type_df["매체"] == selected_channel]
                    filtered_ga_cmp_df = filtered_ga_type_df[filtered_ga_type_df["매체"] == selected_channel]

                    st.session_state.da_cmp_ranking_result["cmp_df"] = filtered_cmp_df
                    st.session_state.da_cmp_ranking_result["ga_cmp_df"] = filtered_ga_cmp_df

                    if submit_button_cmp:

                        detail_cmp_df = ch_ranking_writer.ch_ranking_df(
                            filtered_cmp_df,
                            filtered_ga_cmp_df,
                            '캠페인',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )
                        
                        filtered_detail_cmp_df = detail_cmp_df[detail_cmp_df[grouping_period] == st.session_state.period_set["now"]]

                        sorted_cmp_df, top_cmp_num, cmp_statements = detail_writer.display_top(
                            sort_columns_cmp,
                            sort_orders_cmp,
                            filtered_detail_cmp_df, 
                            st.session_state.overview_result['overview_df'],
                        )

                        st.session_state.da_cmp_ranking_result['top_cmp_detail_df'] = sorted_cmp_df
                        st.session_state.da_cmp_ranking_result['top_num_cmp_detail'] = top_cmp_num
                        st.session_state.da_cmp_ranking_result['cmp_detail_statment'] = cmp_statements

                        st.write('정렬된 상위 ' + str(top_cmp_num) + '개 캠페인')
                        st.write(sorted_cmp_df)

                        for statement in cmp_statements:
                            st.write(statement)

                        try:
                            description_cmp_detail = detail_writer.writer(top_cmp_num, sorted_cmp_df, sort_columns_cmp)

                            st.session_state.da_cmp_ranking_result['description_cmp_detail'] = description_cmp_detail

                            #st.write(description_cmp_detail)
                            bullet_output.display_analysis(description_cmp_detail,sorted_cmp_df.columns.to_list())
                        except:
                            st.session_state.da_cmp_ranking_result['description_cmp_detail'] = "데이터 정합성을 확인해주세요."
                            st.write("데이터 정합성을 확인해주세요.")
                    else:
                        st.write('정렬 기준 지표를 선택한 후, 정렬 적용 버튼을 눌러주세요.')
                        if 'description_cmp_detail' in st.session_state.da_cmp_ranking_result.keys():
                            st.write('정렬된 상위 ' + str(st.session_state.da_cmp_ranking_result['top_num_cmp_detail']) + '개 매체')
                            st.write(st.session_state.da_cmp_ranking_result['top_cmp_detail_df'])

                            for statement in st.session_state.da_cmp_ranking_result['cmp_detail_statment']:
                                st.write(statement)
                            #st.write(st.session_state.cmp_ranking_result['description_cmp_detail'])
                            try:
                                bullet_output.display_analysis(st.session_state.da_cmp_ranking_result['description_cmp_detail'],st.session_state.da_cmp_ranking_result['top_cmp_detail_df'].columns.to_list())
                            except:
                                st.write("데이터 정합성을 확인해주세요.")
                with grp_da:
                    st.header("그룹 분석")
                    st.write("분석하고자 하는 캠페인을 선택해주세요.")
                    if 'description_cmp_detail' in st.session_state.da_cmp_ranking_result.keys():
                        st.write("아래는 " + st.session_state.da_cmp_ranking_result["channel"] + "의 캠페인 목록입니다.")
                        
                        selected_campaign = st.selectbox(
                            "캠페인 선택",
                            st.session_state.da_cmp_ranking_result["cmp_df"]["캠페인"].dropna().unique(),
                        )

                        st.session_state.da_grp_ranking_result = {"campaign" : selected_campaign}

                        filtered_grp_df = st.session_state.df_set["used_media"][(st.session_state.df_set["used_media"]["매체"] == st.session_state.da_cmp_ranking_result["channel"]) & (st.session_state.df_set["used_media"]["캠페인"] == selected_campaign)]
                        filtered_ga_grp_df = st.session_state.df_set["used_ga"][(st.session_state.df_set["used_ga"]["매체"] == st.session_state.da_cmp_ranking_result["channel"]) & (st.session_state.df_set["used_ga"]["캠페인"] == selected_campaign)]

                        st.session_state.da_grp_ranking_result["grp_df"] = filtered_grp_df
                        st.session_state.da_grp_ranking_result["ga_grp_df"] = filtered_ga_grp_df

                        detail_grp_df = ch_ranking_writer.ch_ranking_df(
                            filtered_grp_df,
                            filtered_ga_grp_df,
                            '광고그룹',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        filtered_detail_grp_df = detail_grp_df[detail_grp_df[grouping_period] == st.session_state.period_set["now"]]

                        if len(filtered_detail_grp_df) == 0:
                            st.write("이번 기간에는 운영되지 않은 캠페인입니다.")
                        else:
                            sorted_grp_df, top_grp_num, grp_statements = detail_writer.display_top(
                                st.session_state.da_cmp_ranking_result["selected_metrics"],
                                st.session_state.da_cmp_ranking_result["metric_sort_order"],
                                filtered_detail_grp_df, 
                                st.session_state.overview_result['overview_df'],
                            )

                            st.session_state.da_grp_ranking_result['top_grp_detail_df'] = sorted_grp_df
                            st.session_state.da_grp_ranking_result['top_num_grp_detail'] = top_grp_num
                            st.session_state.da_grp_ranking_result['grp_detail_statment'] = grp_statements

                            st.write('정렬된 상위 ' + str(top_grp_num) + '개 광고그룹')
                            st.write(sorted_grp_df)

                            for statement in grp_statements:
                                st.write(statement)

                            try:
                                description_grp_detail = detail_writer.writer(top_grp_num, sorted_grp_df, st.session_state.da_cmp_ranking_result["selected_metrics"])

                                st.session_state.da_grp_ranking_result['description_grp_detail'] = description_grp_detail

                                #st.write(description_grp_detail)
                                bullet_output.display_analysis(description_grp_detail, sorted_grp_df.columns.to_list())
                            except:
                                st.write("데이터 정합성을 확인해주세요.")
                    else:
                        st.write("캠페인 분석 탭을 먼저 실행해주세요.")
                with brnch_da:
                    if brnch_dsply != 0:
                        for brnch in st.session_state.brnch_ranking_result["sort_order"]:
                            if str(brnch) == '정보없음':
                                continue
                            elif brnch in filtered_type_df["소재구분"].dropna().unique():
                                st.subheader(brnch)
                                st.write(st.session_state.brnch_ranking_result["brnch_overview_df_dic"][brnch])
                                with st.expander("전체 지표 별 변화 문구"):
                                    bullet_output.print_dic_bullet(st.session_state.brnch_ranking_result["brnch_overview_st_dic"][brnch])
                                bullet_output.print_dic_bullet(st.session_state.brnch_ranking_result["brnch_overview_st_dic_summary"][brnch])
                            else:
                                continue
                    else:
                        st.write('매체 데이터에서 소재구분 데이터가 없는 기간입니다.')
                with brnch_dtl_da:
                    if brnch_dsply == 0:
                        st.write('매체 데이터에서 소재구분 데이터가 없는 기간입니다.')
                    else:
                        st.header("소재 구분 분석")
                        st.write("분석하고자 하는 소재 구분을 선택해주세요.")
                        selected_br = st.radio(
                            "소재구분 선택",
                            filtered_type_df["소재구분"].dropna().unique()
                        )
                    
                        sort_orders_br = org_sort_orders
                        metrics = st.session_state.overview_result['overview_df'].columns.tolist()

                        for metric in metrics:
                            if metric not in org_sort_orders.keys():
                                sort_orders_br[metric] = False
                            else:
                                pass
                        
                        submit_button_br, sort_columns_br = detail_writer.choose_metric(metrics,1)

                        if submit_button_br:
                            filtered_br_df = filtered_type_df[filtered_type_df["소재구분"] == selected_br]
                            filtered_ga_br_df = filtered_ga_type_df[filtered_ga_type_df["소재구분"] == selected_br]

                            detail_df = ch_ranking_writer.ch_ranking_df(
                                filtered_br_df,
                                filtered_ga_br_df,
                                '소재종류',
                                st.session_state.metric_set,
                                st.session_state.trans_metric_set,
                                grouping_period,
                                st.session_state.condition_set,
                            )
                            
                            filtered_detail_df = detail_df[detail_df[grouping_period] == st.session_state.period_set["now"]]

                            sorted_df, top_num, br_statements = detail_writer.display_top(
                                sort_columns_br,
                                sort_orders_br,
                                filtered_detail_df, 
                                st.session_state.overview_result['overview_df'],
                            )

                            st.session_state.brnch_detail_result = {'top_brnch_detail_df':sorted_df,'top_num_brnch_detail': top_num, 'brnch_detail_statment':br_statements}

                            st.write('정렬된 상위 ' + str(top_num) + '개 소재종류')
                            st.write(sorted_df)

                            for statement in br_statements:
                                st.write(statement)

                            try:
                                description_brnch_detail = detail_writer.writer(top_num, sorted_df, sort_columns_br)

                                st.session_state.brnch_detail_result['description_brnch_detail'] = description_brnch_detail

                                #st.write(description_brnch_detail)
                                bullet_output.display_analysis(description_brnch_detail,sorted_df.columns.to_list())
                            except:
                                st.session_state.brnch_detail_result['description_brnch_detail'] = "데이터 정합성을 확인해주세요."
                                st.write("데이터 정합성을 확인해주세요.")

                        else:
                            st.write('정렬 기준 지표를 선택한 후, 정렬 적용 버튼을 눌러주세요.')
                            if st.session_state.brnch_detail_result is not None:
                                st.write('정렬된 상위 ' + str(st.session_state.brnch_detail_result['top_num_brnch_detail']) + '개 소재종류')
                                st.write(st.session_state.brnch_detail_result['top_brnch_detail_df'])

                                for statement in st.session_state.brnch_detail_result['brnch_detail_statment']:
                                    st.write(statement)
                                #st.write(st.session_state.brnch_detail_result['description_brnch_detail'])
                                try:
                                    bullet_output.display_analysis(st.session_state.brnch_detail_result['description_brnch_detail'],st.session_state.brnch_detail_result['top_brnch_detail_df'].columns.to_list())
                                except:
                                    st.write("데이터 정합성을 확인해주세요.")              
                with kwrd_da:
                    st.header("키워드별 성과 분석")
                    st.write("성과 상위 키워드를 분석합니다.")
                    if "campaign" in st.session_state.da_grp_ranking_result.keys():
                        st.write("선택된 매체 : " + st.session_state.da_cmp_ranking_result["channel"])
                        st.write("선택된 캠페인 : " + st.session_state.da_grp_ranking_result["campaign"])
                        st.write("선택된 지표 : " + ",".join(st.session_state.da_cmp_ranking_result["selected_metrics"]))

                        detail_kwrd_df = ch_ranking_writer.ch_ranking_df(
                            st.session_state.da_grp_ranking_result["grp_df"],
                            st.session_state.da_grp_ranking_result["ga_grp_df"],
                            '소재명/키워드',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        filtered_detail_kwrd_df = detail_kwrd_df[detail_kwrd_df[grouping_period] == st.session_state.period_set["now"]]
                        
                        if len(filtered_detail_kwrd_df) == 0:
                            st.write("이번 기간에는 운영되지 않은 캠페인입니다.")
                        else:
                            keyword_ranking_df = keyword_writer.kwrd_ranking_df(
                                st.session_state.df_set['used_media'],
                                st.session_state.df_set['used_ga'],
                                st.session_state.metric_set,
                                st.session_state.trans_metric_set,
                                grouping_period,
                                st.session_state.condition_set,
                            )

                            kwrd_statements = keyword_writer.writer(
                                filtered_detail_kwrd_df,
                                keyword_ranking_df, 
                                st.session_state.da_cmp_ranking_result["selected_metrics"],
                                st.session_state.da_cmp_ranking_result["metric_sort_order"],
                            )

                    else:
                        st.write("캠페인 분석 탭을 먼저 실행해주세요.")
                
                st.session_state.DA_result["channel"] = selected_channel

        with history_col:
            history = st.tabs(["운영 히스토리"])
            with history[0]:
                filtered_type_df = st.session_state.df_set['used_media']
                filtered_ga_type_df = st.session_state.df_set['used_ga']

                st.write("분석하고자 하는 매체를 선택해주세요.")
                selected_channel = st.selectbox(
                    "매체 선택",
                    filtered_type_df["매체"].dropna().unique()
                )
                
                st.session_state.history_result["channel"] = selected_channel

                filtered_type_history = st.session_state.df_set['used_history'][st.session_state.df_set['used_history']["매체"] == selected_channel]
                st.write(filtered_type_history)

                st.write("지난 기간 : ", st.session_state.period_set["pre"])
                pre_history = history_writer.writer(
                    filtered_type_history,
                    grouping_period,
                    st.session_state.period_set["pre"])
                st.write(pre_history)

                st.write("이번 기간 : ", st.session_state.period_set["now"])
                now_history = history_writer.writer(
                    filtered_type_history,
                    grouping_period,
                    st.session_state.period_set["now"]
                )
                st.write(now_history)

    else:
        with data_col:
            overview, sa_perform, da_perform  = st.tabs(["오버뷰","SA 성과","DA 성과"])
            with overview:

                if st.session_state.overview_result is None:
                    st.subheader('오버뷰')
                    with st.spinner('데이터 분석 중...'):
                        rounded_overview_df = overview_writer.overview_df(st.session_state.df_set['used_media'], st.session_state.df_set['used_ga'], st.session_state.metric_set, st.session_state.trans_metric_set, grouping_period, st.session_state.condition_set, st.session_state.period_set)
                        overview_statement, overview_statement_summary = overview_writer.writer(rounded_overview_df, rounded_overview_df.columns.to_list())
                
                    st.session_state.overview_result = {'overview_df':rounded_overview_df,'overview_statement':overview_statement,'overview_statement_summary':overview_statement_summary}
                    
                    st.write(rounded_overview_df)
                    with st.expander("전체 지표 별 변화 문구"):
                        bullet_output.print_dic_bullet(overview_statement)
                    bullet_output.print_dic_bullet(overview_statement_summary)
                else:
                    st.subheader('오버뷰')
                    st.write(st.session_state.overview_result['overview_df'])
                    with st.expander("전체 지표 별 변화 문구"):
                        bullet_output.print_dic_bullet(st.session_state.overview_result['overview_statement'])
                    bullet_output.print_dic_bullet(st.session_state.overview_result['overview_statement_summary'])

                
                if st.session_state.ch_ranking_result is None:
                    ch_ranking_df = ch_ranking_writer.ch_ranking_df(
                        st.session_state.df_set['used_media'],
                        st.session_state.df_set['used_ga'],
                        '매체',
                        st.session_state.metric_set,
                        st.session_state.trans_metric_set,
                        grouping_period,
                        st.session_state.condition_set,
                    )
                    

                    now_period_result, sort_order = ch_ranking_writer.display_period_data(
                        st.session_state.period_set["now"],
                        ch_ranking_df,
                        st.session_state.overview_result['overview_df'],
                        '매체',
                        grouping_period,
                        None
                    )


                    st.session_state.ch_ranking_result = {"now_result_df":now_period_result}

                    pre_period_result, _ = ch_ranking_writer.display_period_data(
                        st.session_state.period_set["pre"],
                        ch_ranking_df,
                        st.session_state.overview_result['overview_df'],
                        '매체',
                        grouping_period,
                        sort_order
                    )
                    

                    st.session_state.ch_ranking_result["pre_result_df"] = pre_period_result

                    st.session_state.ch_ranking_result["sort_order"] = sort_order
                    channels = [x for x in now_period_result['매체'].unique() if x != '합계']

                    ch_overview_df_dic = {}
                    ch_overview_st_dic = {}
                    ch_overview_st_dic_summary = {}
                    with st.spinner('데이터 분석 중...'):
                        for channel in channels:
                            if str(channel) == '정보없음':
                                continue
                            rounded_overview_ch_df = ch_ranking_writer.ch_df(
                                ch_ranking_df, '매체', channel, 
                                grouping_period,
                                st.session_state.period_set,
                                st.session_state.condition_set,
                            )
                            overview_ch_statement, overview_ch_statement_summary = overview_writer.writer(rounded_overview_ch_df, rounded_overview_ch_df.columns.to_list())
                            
                            ch_overview_df_dic[channel] = rounded_overview_ch_df
                            ch_overview_st_dic[channel] = overview_ch_statement
                            ch_overview_st_dic_summary[channel] = overview_ch_statement_summary

                    st.session_state.ch_ranking_result["ch_overview_df_dic"] = ch_overview_df_dic
                    st.session_state.ch_ranking_result["ch_overview_st_dic"] = ch_overview_st_dic
                    st.session_state.ch_ranking_result["ch_overview_st_dic_summary"] = ch_overview_st_dic_summary
                else:
                    pass
                
                brnch_dsply = 1

                if st.session_state.df_set['used_media']['소재구분'].isnull().all():
                    brnch_dsply = 0
                    #st.write('매체 데이터에서 소재구분 데이터가 없는 기간입니다.')
                else:
                    if st.session_state.brnch_ranking_result is None:
                        brnch_ranking_df = ch_ranking_writer.ch_ranking_df(
                            st.session_state.df_set['used_media'],
                            st.session_state.df_set['used_ga'],
                            '소재구분',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        now_period_result, sort_order = ch_ranking_writer.display_period_data(
                                st.session_state.period_set["now"],
                                brnch_ranking_df,
                                st.session_state.overview_result['overview_df'],
                                '소재구분',
                                grouping_period,
                                None
                            )

                        st.session_state.brnch_ranking_result = {"now_result_df":now_period_result}
                        

                        pre_period_result, _ = ch_ranking_writer.display_period_data(
                                st.session_state.period_set["pre"],
                                brnch_ranking_df,
                                st.session_state.overview_result['overview_df'],
                                '소재구분',
                                grouping_period,
                                sort_order
                            )

                        st.session_state.brnch_ranking_result["pre_result_df"] = pre_period_result

                        st.session_state.brnch_ranking_result["sort_order"] = sort_order
                        brnchs = [x for x in now_period_result['소재구분'].unique() if x != '합계']

                        brnch_overview_df_dic = {}
                        brnch_overview_st_dic = {}
                        brnch_overview_st_dic_summary = {}
                        with st.spinner('데이터 분석 중...'):
                            for brnch in brnchs:
                                if str(brnch) == '정보없음':
                                    continue
                                rounded_overview_brnch_df = ch_ranking_writer.ch_df(
                                    brnch_ranking_df, '소재구분', brnch, 
                                    grouping_period,
                                    st.session_state.period_set,
                                    st.session_state.condition_set,
                                )
                                overview_brnch_statement, overview_brnch_statement_summary = overview_writer.writer(rounded_overview_brnch_df, rounded_overview_brnch_df.columns.to_list())
                                
                                brnch_overview_df_dic[brnch] = rounded_overview_brnch_df
                                brnch_overview_st_dic[brnch] = overview_brnch_statement
                                brnch_overview_st_dic_summary[brnch] = overview_brnch_statement_summary


                        st.session_state.brnch_ranking_result["brnch_overview_df_dic"] = brnch_overview_df_dic
                        st.session_state.brnch_ranking_result["brnch_overview_st_dic"] = brnch_overview_st_dic
                        st.session_state.brnch_ranking_result["brnch_overview_st_dic_summary"] = brnch_overview_st_dic_summary

            with sa_perform:
                selected_ad_type = "SA"
                st.session_state.SA_result = {"ad_type":selected_ad_type}

                filtered_type_df = st.session_state.df_set['used_media'][st.session_state.df_set['used_media']["광고유형"] == selected_ad_type]
                filtered_ga_type_df = st.session_state.df_set['used_ga'][st.session_state.df_set['used_ga']["광고유형"] == selected_ad_type]

                st.write("분석하고자 하는 매체를 선택해주세요.")
                selected_channel = st.selectbox(
                    "매체 선택",
                    filtered_type_df["매체"].dropna().unique()
                )
                
                st.session_state.SA_result["channel"] = selected_channel
                st.session_state.cmp_ranking_result["channel"] = selected_channel

                overview_sa, cmp_sa, grp_sa, kwrd_sa  = st.tabs(["전체 성과 분석","캠페인 분석","그룹 분석", "성과 상위 키워드 분석"])
                with overview_sa:
                    st.subheader(selected_channel)
                    st.write(st.session_state.ch_ranking_result["ch_overview_df_dic"][selected_channel])
                    with st.expander("전체 지표 별 변화 문구"):
                        bullet_output.print_dic_bullet(st.session_state.ch_ranking_result["ch_overview_st_dic"][selected_channel])
                    bullet_output.print_dic_bullet(st.session_state.ch_ranking_result["ch_overview_st_dic_summary"][selected_channel])

                with cmp_sa:
                    sort_orders_cmp = org_sort_orders
                    metrics = st.session_state.overview_result['overview_df'].columns.tolist()

                    for metric in metrics:
                        if metric not in org_sort_orders.keys():
                            sort_orders_cmp[metric] = False
                        else:
                            pass
                    
                    submit_button_cmp, sort_columns_cmp = detail_writer.choose_metric(metrics,2)

                    st.session_state.cmp_ranking_result["submit_button"] = submit_button_cmp
                    st.session_state.cmp_ranking_result["metric_sort_order"] = sort_orders_cmp
                    st.session_state.cmp_ranking_result["selected_metrics"] = sort_columns_cmp

                    filtered_cmp_df = filtered_type_df[filtered_type_df["매체"] == selected_channel]
                    filtered_ga_cmp_df = filtered_ga_type_df[filtered_ga_type_df["매체"] == selected_channel]

                    st.session_state.cmp_ranking_result["cmp_df"] = filtered_cmp_df
                    st.session_state.cmp_ranking_result["ga_cmp_df"] = filtered_ga_cmp_df

                    if submit_button_cmp:

                        detail_cmp_df = ch_ranking_writer.ch_ranking_df(
                            filtered_cmp_df,
                            filtered_ga_cmp_df,
                            '캠페인',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )
                        
                        filtered_detail_cmp_df = detail_cmp_df[detail_cmp_df[grouping_period] == st.session_state.period_set["now"]]

                        sorted_cmp_df, top_cmp_num, cmp_statements = detail_writer.display_top(
                            sort_columns_cmp,
                            sort_orders_cmp,
                            filtered_detail_cmp_df, 
                            st.session_state.overview_result['overview_df'],
                        )

                        st.session_state.cmp_ranking_result['top_cmp_detail_df'] = sorted_cmp_df
                        st.session_state.cmp_ranking_result['top_num_cmp_detail'] = top_cmp_num
                        st.session_state.cmp_ranking_result['cmp_detail_statment'] = cmp_statements

                        st.write('정렬된 상위 ' + str(top_cmp_num) + '개 캠페인')
                        st.write(sorted_cmp_df)

                        for statement in cmp_statements:
                            st.write(statement)

                        try:
                            description_cmp_detail = detail_writer.writer(top_cmp_num, sorted_cmp_df, sort_columns_cmp)

                            st.session_state.cmp_ranking_result['description_cmp_detail'] = description_cmp_detail

                            #st.write(description_cmp_detail)
                            bullet_output.display_analysis(description_cmp_detail,sorted_cmp_df.columns.to_list())
                        except:
                            st.session_state.cmp_ranking_result['description_cmp_detail'] = "데이터 정합성을 확인해주세요."
                            st.write("데이터 정합성을 확인해주세요.")
                    else:
                        st.write('정렬 기준 지표를 선택한 후, 정렬 적용 버튼을 눌러주세요.')
                        if 'description_cmp_detail' in st.session_state.cmp_ranking_result.keys():
                            st.write('정렬된 상위 ' + str(st.session_state.cmp_ranking_result['top_num_cmp_detail']) + '개 매체')
                            st.write(st.session_state.cmp_ranking_result['top_cmp_detail_df'])

                            for statement in st.session_state.cmp_ranking_result['cmp_detail_statment']:
                                st.write(statement)
                            #st.write(st.session_state.cmp_ranking_result['description_cmp_detail'])
                            try:
                                bullet_output.display_analysis(st.session_state.cmp_ranking_result['description_cmp_detail'],st.session_state.cmp_ranking_result['top_cmp_detail_df'].columns.to_list())
                            except:
                                st.write("데이터 정합성을 확인해주세요.")
                with grp_sa:
                    st.header("그룹 분석")
                    st.write("분석하고자 하는 캠페인을 선택해주세요.")
                    if 'description_cmp_detail' in st.session_state.cmp_ranking_result.keys():
                        st.write("아래는 " + st.session_state.cmp_ranking_result["channel"] + "의 캠페인 목록입니다.")
                        
                        selected_campaign = st.selectbox(
                            "캠페인 선택",
                            st.session_state.cmp_ranking_result["cmp_df"]["캠페인"].dropna().unique(),
                        )

                        st.session_state.grp_ranking_result = {"campaign" : selected_campaign}

                        filtered_grp_df = st.session_state.df_set["used_media"][(st.session_state.df_set["used_media"]["매체"] == st.session_state.cmp_ranking_result["channel"]) & (st.session_state.df_set["used_media"]["캠페인"] == selected_campaign)]
                        filtered_ga_grp_df = st.session_state.df_set["used_ga"][(st.session_state.df_set["used_ga"]["매체"] == st.session_state.cmp_ranking_result["channel"]) & (st.session_state.df_set["used_ga"]["캠페인"] == selected_campaign)]

                        st.session_state.grp_ranking_result["grp_df"] = filtered_grp_df
                        st.session_state.grp_ranking_result["ga_grp_df"] = filtered_ga_grp_df

                        detail_grp_df = ch_ranking_writer.ch_ranking_df(
                            filtered_grp_df,
                            filtered_ga_grp_df,
                            '광고그룹',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        filtered_detail_grp_df = detail_grp_df[detail_grp_df[grouping_period] == st.session_state.period_set["now"]]

                        if len(filtered_detail_grp_df) == 0:
                            st.write("이번 기간에는 운영되지 않은 캠페인입니다.")
                        else:
                            sorted_grp_df, top_grp_num, grp_statements = detail_writer.display_top(
                                st.session_state.cmp_ranking_result["selected_metrics"],
                                st.session_state.cmp_ranking_result["metric_sort_order"],
                                filtered_detail_grp_df, 
                                st.session_state.overview_result['overview_df'],
                            )

                            st.session_state.grp_ranking_result['top_grp_detail_df'] = sorted_grp_df
                            st.session_state.grp_ranking_result['top_num_grp_detail'] = top_grp_num
                            st.session_state.grp_ranking_result['grp_detail_statment'] = grp_statements

                            st.write('정렬된 상위 ' + str(top_grp_num) + '개 광고그룹')
                            st.write(sorted_grp_df)

                            for statement in grp_statements:
                                st.write(statement)

                            try:
                                description_grp_detail = detail_writer.writer(top_grp_num, sorted_grp_df, st.session_state.cmp_ranking_result["selected_metrics"])

                                st.session_state.grp_ranking_result['description_grp_detail'] = description_grp_detail

                                #st.write(description_grp_detail)
                                bullet_output.display_analysis(description_grp_detail, sorted_grp_df.columns.to_list())
                            except:
                                st.write("데이터 정합성을 확인해주세요.")
                    else:
                        st.write("캠페인 분석 탭을 먼저 실행해주세요.")
                with kwrd_sa:
                    st.header("키워드별 성과 분석")
                    st.write("성과 상위 키워드를 분석합니다.")
                    if "campaign" in st.session_state.grp_ranking_result.keys():
                        st.write("선택된 매체 : " + st.session_state.cmp_ranking_result["channel"])
                        st.write("선택된 캠페인 : " + st.session_state.grp_ranking_result["campaign"])
                        st.write("선택된 지표 : " + ",".join(st.session_state.cmp_ranking_result["selected_metrics"]))

                        detail_kwrd_df = ch_ranking_writer.ch_ranking_df(
                            st.session_state.grp_ranking_result["grp_df"],
                            st.session_state.grp_ranking_result["ga_grp_df"],
                            '소재명/키워드',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        filtered_detail_kwrd_df = detail_kwrd_df[detail_kwrd_df[grouping_period] == st.session_state.period_set["now"]]
                        
                        if len(filtered_detail_kwrd_df) == 0:
                            st.write("이번 기간에는 운영되지 않은 캠페인입니다.")
                        else:
                            keyword_ranking_df = keyword_writer.kwrd_ranking_df(
                                st.session_state.df_set['used_media'],
                                st.session_state.df_set['used_ga'],
                                st.session_state.metric_set,
                                st.session_state.trans_metric_set,
                                grouping_period,
                                st.session_state.condition_set,
                            )

                            kwrd_statements = keyword_writer.writer(
                                filtered_detail_kwrd_df,
                                keyword_ranking_df, 
                                st.session_state.cmp_ranking_result["selected_metrics"],
                                st.session_state.cmp_ranking_result["metric_sort_order"],
                            )

                    else:
                        st.write("캠페인 분석 탭을 먼저 실행해주세요.")
            with da_perform:
                selected_ad_type = "DA"
                st.session_state.DA_result = {"ad_type":selected_ad_type}

                filtered_type_df = st.session_state.df_set['used_media'][st.session_state.df_set['used_media']["광고유형"] == selected_ad_type]
                filtered_ga_type_df = st.session_state.df_set['used_ga'][st.session_state.df_set['used_ga']["광고유형"] == selected_ad_type]

                st.write("분석하고자 하는 매체를 선택해주세요.")
                selected_channel = st.selectbox(
                    "매체 선택",
                    filtered_type_df["매체"].dropna().unique()
                )
                
                st.session_state.da_cmp_ranking_result["channel"] = selected_channel
                overview_da, cmp_da, grp_da, brnch_da, brnch_dtl_da, kwrd_da  = st.tabs(["전체 성과 분석","캠페인 분석","그룹 분석", "소재구분 분석", "소재종류 분석", "성과 상위 소재 분석"])
                with overview_da:
                    st.subheader(selected_channel)
                    st.write(st.session_state.ch_ranking_result["ch_overview_df_dic"][selected_channel])
                    with st.expander("전체 지표 별 변화 문구"):
                        bullet_output.print_dic_bullet(st.session_state.ch_ranking_result["ch_overview_st_dic"][selected_channel])
                    bullet_output.print_dic_bullet(st.session_state.ch_ranking_result["ch_overview_st_dic_summary"][selected_channel])
                with cmp_da:
                    sort_orders_cmp = org_sort_orders
                    metrics = st.session_state.overview_result['overview_df'].columns.tolist()

                    for metric in metrics:
                        if metric not in org_sort_orders.keys():
                            sort_orders_cmp[metric] = False
                        else:
                            pass
                    
                    submit_button_cmp, sort_columns_cmp = detail_writer.choose_metric(metrics,3)

                    st.session_state.da_cmp_ranking_result["submit_button"] = submit_button_cmp
                    st.session_state.da_cmp_ranking_result["metric_sort_order"] = sort_orders_cmp
                    st.session_state.da_cmp_ranking_result["selected_metrics"] = sort_columns_cmp

                    filtered_cmp_df = filtered_type_df[filtered_type_df["매체"] == selected_channel]
                    filtered_ga_cmp_df = filtered_ga_type_df[filtered_ga_type_df["매체"] == selected_channel]

                    st.session_state.da_cmp_ranking_result["cmp_df"] = filtered_cmp_df
                    st.session_state.da_cmp_ranking_result["ga_cmp_df"] = filtered_ga_cmp_df

                    if submit_button_cmp:

                        detail_cmp_df = ch_ranking_writer.ch_ranking_df(
                            filtered_cmp_df,
                            filtered_ga_cmp_df,
                            '캠페인',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )
                        
                        filtered_detail_cmp_df = detail_cmp_df[detail_cmp_df[grouping_period] == st.session_state.period_set["now"]]

                        sorted_cmp_df, top_cmp_num, cmp_statements = detail_writer.display_top(
                            sort_columns_cmp,
                            sort_orders_cmp,
                            filtered_detail_cmp_df, 
                            st.session_state.overview_result['overview_df'],
                        )

                        st.session_state.da_cmp_ranking_result['top_cmp_detail_df'] = sorted_cmp_df
                        st.session_state.da_cmp_ranking_result['top_num_cmp_detail'] = top_cmp_num
                        st.session_state.da_cmp_ranking_result['cmp_detail_statment'] = cmp_statements

                        st.write('정렬된 상위 ' + str(top_cmp_num) + '개 캠페인')
                        st.write(sorted_cmp_df)

                        for statement in cmp_statements:
                            st.write(statement)

                        try:
                            description_cmp_detail = detail_writer.writer(top_cmp_num, sorted_cmp_df, sort_columns_cmp)

                            st.session_state.da_cmp_ranking_result['description_cmp_detail'] = description_cmp_detail

                            #st.write(description_cmp_detail)
                            bullet_output.display_analysis(description_cmp_detail,sorted_cmp_df.columns.to_list())
                        except:
                            st.session_state.da_cmp_ranking_result['description_cmp_detail'] = "데이터 정합성을 확인해주세요."
                            st.write("데이터 정합성을 확인해주세요.")
                    else:
                        st.write('정렬 기준 지표를 선택한 후, 정렬 적용 버튼을 눌러주세요.')
                        if 'description_cmp_detail' in st.session_state.da_cmp_ranking_result.keys():
                            st.write('정렬된 상위 ' + str(st.session_state.da_cmp_ranking_result['top_num_cmp_detail']) + '개 매체')
                            st.write(st.session_state.da_cmp_ranking_result['top_cmp_detail_df'])

                            for statement in st.session_state.da_cmp_ranking_result['cmp_detail_statment']:
                                st.write(statement)
                            #st.write(st.session_state.cmp_ranking_result['description_cmp_detail'])
                            try:
                                bullet_output.display_analysis(st.session_state.da_cmp_ranking_result['description_cmp_detail'],st.session_state.da_cmp_ranking_result['top_cmp_detail_df'].columns.to_list())
                            except:
                                st.write("데이터 정합성을 확인해주세요.")
                with grp_da:
                    st.header("그룹 분석")
                    st.write("분석하고자 하는 캠페인을 선택해주세요.")
                    if 'description_cmp_detail' in st.session_state.da_cmp_ranking_result.keys():
                        st.write("아래는 " + st.session_state.da_cmp_ranking_result["channel"] + "의 캠페인 목록입니다.")
                        
                        selected_campaign = st.selectbox(
                            "캠페인 선택",
                            st.session_state.da_cmp_ranking_result["cmp_df"]["캠페인"].dropna().unique(),
                        )

                        st.session_state.da_grp_ranking_result = {"campaign" : selected_campaign}

                        filtered_grp_df = st.session_state.df_set["used_media"][(st.session_state.df_set["used_media"]["매체"] == st.session_state.da_cmp_ranking_result["channel"]) & (st.session_state.df_set["used_media"]["캠페인"] == selected_campaign)]
                        filtered_ga_grp_df = st.session_state.df_set["used_ga"][(st.session_state.df_set["used_ga"]["매체"] == st.session_state.da_cmp_ranking_result["channel"]) & (st.session_state.df_set["used_ga"]["캠페인"] == selected_campaign)]

                        st.session_state.da_grp_ranking_result["grp_df"] = filtered_grp_df
                        st.session_state.da_grp_ranking_result["ga_grp_df"] = filtered_ga_grp_df

                        detail_grp_df = ch_ranking_writer.ch_ranking_df(
                            filtered_grp_df,
                            filtered_ga_grp_df,
                            '광고그룹',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        filtered_detail_grp_df = detail_grp_df[detail_grp_df[grouping_period] == st.session_state.period_set["now"]]

                        if len(filtered_detail_grp_df) == 0:
                            st.write("이번 기간에는 운영되지 않은 캠페인입니다.")
                        else:
                            sorted_grp_df, top_grp_num, grp_statements = detail_writer.display_top(
                                st.session_state.da_cmp_ranking_result["selected_metrics"],
                                st.session_state.da_cmp_ranking_result["metric_sort_order"],
                                filtered_detail_grp_df, 
                                st.session_state.overview_result['overview_df'],
                            )

                            st.session_state.da_grp_ranking_result['top_grp_detail_df'] = sorted_grp_df
                            st.session_state.da_grp_ranking_result['top_num_grp_detail'] = top_grp_num
                            st.session_state.da_grp_ranking_result['grp_detail_statment'] = grp_statements

                            st.write('정렬된 상위 ' + str(top_grp_num) + '개 광고그룹')
                            st.write(sorted_grp_df)

                            for statement in grp_statements:
                                st.write(statement)

                            try:
                                description_grp_detail = detail_writer.writer(top_grp_num, sorted_grp_df, st.session_state.da_cmp_ranking_result["selected_metrics"])

                                st.session_state.da_grp_ranking_result['description_grp_detail'] = description_grp_detail

                                #st.write(description_grp_detail)
                                bullet_output.display_analysis(description_grp_detail, sorted_grp_df.columns.to_list())
                            except:
                                st.write("데이터 정합성을 확인해주세요.")
                    else:
                        st.write("캠페인 분석 탭을 먼저 실행해주세요.")
                with brnch_da:
                    if brnch_dsply != 0:
                        for brnch in st.session_state.brnch_ranking_result["sort_order"]:
                            if str(brnch) == '정보없음':
                                continue
                            elif brnch in filtered_type_df["소재구분"].dropna().unique():
                                st.subheader(brnch)
                                st.write(st.session_state.brnch_ranking_result["brnch_overview_df_dic"][brnch])
                                with st.expander("전체 지표 별 변화 문구"):
                                    bullet_output.print_dic_bullet(st.session_state.brnch_ranking_result["brnch_overview_st_dic"][brnch])
                                bullet_output.print_dic_bullet(st.session_state.brnch_ranking_result["brnch_overview_st_dic_summary"][brnch])
                            else:
                                continue
                    else:
                        st.write('매체 데이터에서 소재구분 데이터가 없는 기간입니다.')
                with brnch_dtl_da:
                    if brnch_dsply == 0:
                        st.write('매체 데이터에서 소재구분 데이터가 없는 기간입니다.')
                    else:
                        st.header("소재 구분 분석")
                        st.write("분석하고자 하는 소재 구분을 선택해주세요.")
                        selected_br = st.radio(
                            "소재구분 선택",
                            filtered_type_df["소재구분"].dropna().unique()
                        )
                    
                        sort_orders_br = org_sort_orders
                        metrics = st.session_state.overview_result['overview_df'].columns.tolist()

                        for metric in metrics:
                            if metric not in org_sort_orders.keys():
                                sort_orders_br[metric] = False
                            else:
                                pass
                        
                        submit_button_br, sort_columns_br = detail_writer.choose_metric(metrics,1)

                        if submit_button_br:
                            filtered_br_df = filtered_type_df[filtered_type_df["소재구분"] == selected_br]
                            filtered_ga_br_df = filtered_ga_type_df[filtered_ga_type_df["소재구분"] == selected_br]

                            detail_df = ch_ranking_writer.ch_ranking_df(
                                filtered_br_df,
                                filtered_ga_br_df,
                                '소재종류',
                                st.session_state.metric_set,
                                st.session_state.trans_metric_set,
                                grouping_period,
                                st.session_state.condition_set,
                            )
                            
                            filtered_detail_df = detail_df[detail_df[grouping_period] == st.session_state.period_set["now"]]

                            sorted_df, top_num, br_statements = detail_writer.display_top(
                                sort_columns_br,
                                sort_orders_br,
                                filtered_detail_df, 
                                st.session_state.overview_result['overview_df'],
                            )

                            st.session_state.brnch_detail_result = {'top_brnch_detail_df':sorted_df,'top_num_brnch_detail': top_num, 'brnch_detail_statment':br_statements}

                            st.write('정렬된 상위 ' + str(top_num) + '개 소재종류')
                            st.write(sorted_df)

                            for statement in br_statements:
                                st.write(statement)

                            try:
                                description_brnch_detail = detail_writer.writer(top_num, sorted_df, sort_columns_br)

                                st.session_state.brnch_detail_result['description_brnch_detail'] = description_brnch_detail

                                #st.write(description_brnch_detail)
                                bullet_output.display_analysis(description_brnch_detail,sorted_df.columns.to_list())
                            except:
                                st.session_state.brnch_detail_result['description_brnch_detail'] = "데이터 정합성을 확인해주세요."
                                st.write("데이터 정합성을 확인해주세요.")

                        else:
                            st.write('정렬 기준 지표를 선택한 후, 정렬 적용 버튼을 눌러주세요.')
                            if st.session_state.brnch_detail_result is not None:
                                st.write('정렬된 상위 ' + str(st.session_state.brnch_detail_result['top_num_brnch_detail']) + '개 소재종류')
                                st.write(st.session_state.brnch_detail_result['top_brnch_detail_df'])

                                for statement in st.session_state.brnch_detail_result['brnch_detail_statment']:
                                    st.write(statement)
                                #st.write(st.session_state.brnch_detail_result['description_brnch_detail'])
                                try:
                                    bullet_output.display_analysis(st.session_state.brnch_detail_result['description_brnch_detail'],st.session_state.brnch_detail_result['top_brnch_detail_df'].columns.to_list())
                                except:
                                    st.write("데이터 정합성을 확인해주세요.")              
                with kwrd_da:
                    st.header("키워드별 성과 분석")
                    st.write("성과 상위 키워드를 분석합니다.")
                    if "campaign" in st.session_state.da_grp_ranking_result.keys():
                        st.write("선택된 매체 : " + st.session_state.da_cmp_ranking_result["channel"])
                        st.write("선택된 캠페인 : " + st.session_state.da_grp_ranking_result["campaign"])
                        st.write("선택된 지표 : " + ",".join(st.session_state.da_cmp_ranking_result["selected_metrics"]))

                        detail_kwrd_df = ch_ranking_writer.ch_ranking_df(
                            st.session_state.da_grp_ranking_result["grp_df"],
                            st.session_state.da_grp_ranking_result["ga_grp_df"],
                            '소재명/키워드',
                            st.session_state.metric_set,
                            st.session_state.trans_metric_set,
                            grouping_period,
                            st.session_state.condition_set,
                        )

                        filtered_detail_kwrd_df = detail_kwrd_df[detail_kwrd_df[grouping_period] == st.session_state.period_set["now"]]
                        
                        if len(filtered_detail_kwrd_df) == 0:
                            st.write("이번 기간에는 운영되지 않은 캠페인입니다.")
                        else:
                            keyword_ranking_df = keyword_writer.kwrd_ranking_df(
                                st.session_state.df_set['used_media'],
                                st.session_state.df_set['used_ga'],
                                st.session_state.metric_set,
                                st.session_state.trans_metric_set,
                                grouping_period,
                                st.session_state.condition_set,
                            )

                            kwrd_statements = keyword_writer.writer(
                                filtered_detail_kwrd_df,
                                keyword_ranking_df, 
                                st.session_state.da_cmp_ranking_result["selected_metrics"],
                                st.session_state.da_cmp_ranking_result["metric_sort_order"],
                            )

                    else:
                        st.write("캠페인 분석 탭을 먼저 실행해주세요.")
                
                st.session_state.DA_result["channel"] = selected_channel

        with history_col:
            history = st.tabs(["운영 히스토리"])
            with history[0]:
                filtered_type_df = st.session_state.df_set['used_media']
                filtered_ga_type_df = st.session_state.df_set['used_ga']

                st.write("분석하고자 하는 매체를 선택해주세요.")
                selected_channel = st.selectbox(
                    "매체 선택",
                    filtered_type_df["매체"].dropna().unique()
                )
                
                st.session_state.history_result["channel"] = selected_channel

                filtered_type_history = st.session_state.df_set['used_history'][st.session_state.df_set['used_history']["매체"] == selected_channel]
                st.write(filtered_type_history)

                st.write("지난 기간 : ", st.session_state.period_set["pre"])
                pre_history = history_writer.writer(
                    filtered_type_history,
                    grouping_period,
                    st.session_state.period_set["pre"])
                st.write(pre_history)

                st.write("이번 기간 : ", st.session_state.period_set["now"])
                now_history = history_writer.writer(
                    filtered_type_history,
                    grouping_period,
                    st.session_state.period_set["now"]
                )
                st.write(now_history)
